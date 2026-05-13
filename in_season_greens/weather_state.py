import httpx
from collections import defaultdict
from datetime import date, timedelta
import statistics
import time
from threading import Lock


class WeatherState:

    _cache: dict = {}
    _cache_lock = Lock()

    # Cache durations (seconds)
    _FORECAST_TTL = 60 * 30          # 30 minutes
    _HISTORICAL_TTL = 60 * 60 * 24  # 24 hours

    @staticmethod
    def _make_cache_key(url: str, params: dict) -> tuple:

        return (
            url,
            tuple(sorted((k, str(v)) for k, v in params.items()))
        )

    @classmethod
    def _get_cached_response(
        cls,
        url: str,
        params: dict,
        ttl: int,
    ) -> dict | None:

        key = cls._make_cache_key(url, params)
        now = time.time()

      
        with cls._cache_lock:
            cached = cls._cache.get(key)
            if cached:
                expires_at, data = cached
                if now < expires_at:
                    return data

        with httpx.Client() as client:
            resp = client.get(
                url,
                params=params,
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()

        with cls._cache_lock:
            cls._cache[key] = (now + ttl, data)

        return data

    @staticmethod
    def _get_historical_normal(
        lat: float,
        lon: float,
        variable: str,
        years: int = 30,
    ) -> tuple[float, float] | None:

        today = date.today()

        start_year = today.year - years
        try:
            start_date = date(start_year, today.month, today.day)
        except ValueError:
            start_date = date(start_year, today.month, today.day - 1)

        start_date = max(start_date, date(1940, 1, 1))
        end_date = today - timedelta(days=1)

        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "daily": variable,
            "timezone": "auto",
        }

        try:
            data = WeatherState._get_cached_response(
                "https://archive-api.open-meteo.com/v1/archive",
                params,
                WeatherState._HISTORICAL_TTL,
            )

            dates: list[str] = data["daily"]["time"]
            values: list[float | None] = data["daily"][variable]

            target_md = (today.month, today.day)
            daily_values: list[float] = []

            for d_str, val in zip(dates, values):
                d = date.fromisoformat(d_str)

                if (d.month, d.day) == target_md and val is not None:
                    daily_values.append(val)

            if len(daily_values) < 5:
                return None

            mean = statistics.mean(daily_values)
            stdev = (
                statistics.stdev(daily_values)
                if len(daily_values) > 1
                else 1.0
            )

            return mean, stdev

        except Exception as e:
            print(f"[Historical Normal Error] {e}")
            return None

    @staticmethod
    def _get_today_forecast(
        lat: float,
        lon: float,
        variables: list[str],
    ) -> dict:
        """
        Fetch today's forecast values for a list of daily variables.
        """

        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ",".join(variables),
            "timezone": "auto",
            "forecast_days": 1,
        }

        try:
            data = WeatherState._get_cached_response(
                "https://api.open-meteo.com/v1/forecast",
                params,
                WeatherState._FORECAST_TTL,
            )

            return {
                var: data["daily"][var][0]
                for var in variables
            }

        except Exception as e:
            print(f"[Forecast Error] {e}")
            return {}

    @staticmethod
    def get_avg_temp(lat: float, lon: float) -> str:
        """
        Returns today's temp with a label comparing it to the 30-year normal,
        e.g. "14.2°C · Above Normal"
        """

        forecast = WeatherState._get_today_forecast(
            lat,
            lon,
            ["temperature_2m_mean"],
        )

        today_temp = forecast.get("temperature_2m_mean")

        if today_temp is None:
            return "N/A"

        normal = WeatherState._get_historical_normal(
            lat,
            lon,
            "temperature_2m_mean",
        )

        temp_str = f"{today_temp:.1f}°C"

        if normal is None:
            return temp_str

        mean, stdev = normal
        deviation = today_temp - mean

        if deviation > stdev:
            label = "Above Normal"
        elif deviation < -stdev:
            label = "Below Normal"
        else:
            label = "Normal"

        return f"{temp_str} · {label}"

    @staticmethod
    def get_rain_outlook(lat: float, lon: float) -> str:
        """
        Returns a rain label comparing today's forecast precipitation
        to the 30-year normal for this calendar date.
        """

        forecast = WeatherState._get_today_forecast(
            lat,
            lon,
            ["precipitation_sum"],
        )

        today_rain = forecast.get("precipitation_sum")

        if today_rain is None:
            return "Unknown"

        if today_rain == 0:
            normal = WeatherState._get_historical_normal(
                lat,
                lon,
                "precipitation_sum",
            )

            if normal and normal[0] > 1.0:
                return "Drier Than Normal"

            return "Dry"

        normal = WeatherState._get_historical_normal(
            lat,
            lon,
            "precipitation_sum",
        )

        if normal is None:
            if today_rain < 2.0:
                return "Light Rain"
            elif today_rain < 10.0:
                return "Normal"
            else:
                return "Heavy Rain"

        mean, stdev = normal

        if mean < 0.5:
            if today_rain < 2.0:
                return "Light Rain"
            elif today_rain < 10.0:
                return "Moderate Rain"
            else:
                return "Heavy Rain"

        deviation = today_rain - mean

        if deviation > stdev:
            return "Wetter Than Normal"
        elif deviation < -stdev:
            return "Drier Than Normal"
        else:
            return "Normal"

    @staticmethod
    def get_harvest_outlook(lat: float, lon: float) -> str:
        """
        Derives harvest outlook from three agronomic signals compared against
        their 30-year historical normals for this calendar date:
          - Growing Degree Days (GDD)
          - Soil moisture (9–27cm)
          - Soil temperature (6cm)
        """

        today = date.today()
        target_md = (today.month, today.day)


        try:
            forecast_params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "growing_degree_days_base_0_limit_30",
                "hourly": "soil_moisture_9_27cm,soil_temperature_6cm",
                "timezone": "auto",
                "forecast_days": 1,
            }

            forecast = WeatherState._get_cached_response(
                "https://agri-api.open-meteo.com/v1/forecast",
                forecast_params,
                WeatherState._FORECAST_TTL,
            )

            gdd_today = forecast["daily"][
                "growing_degree_days_base_0_limit_30"
            ][0]

            hourly_moisture = forecast["hourly"][
                "soil_moisture_9_27cm"
            ]

            hourly_soil_temp = forecast["hourly"][
                "soil_temperature_6cm"
            ]

            soil_moisture_today = statistics.mean(
                v for v in hourly_moisture if v is not None
            )

            soil_temp_today = statistics.mean(
                v for v in hourly_soil_temp if v is not None
            )

        except Exception as e:
            print(f"[Harvest Forecast Error] {e}")
            return "Unavailable"


        start_year = today.year - 30

        try:
            archive_start = date(
                start_year,
                today.month,
                today.day,
            )

        except ValueError:
            archive_start = date(
                start_year,
                today.month,
                today.day - 1,
            )

        archive_end = today - timedelta(days=1)

        try:
            hist_params = {
                "latitude": lat,
                "longitude": lon,
                "start_date": str(archive_start),
                "end_date": str(archive_end),
                "daily": "growing_degree_days_base_0_limit_30",
                "hourly": (
                    "soil_moisture_9_27cm,"
                    "soil_temperature_6cm"
                ),
                "timezone": "auto",
            }

            hist = WeatherState._get_cached_response(
                "https://archive-api.open-meteo.com/v1/archive",
                hist_params,
                WeatherState._HISTORICAL_TTL,
            )

            hist_gdd: list[float] = []

            for d_str, gdd in zip(
                hist["daily"]["time"],
                hist["daily"][
                    "growing_degree_days_base_0_limit_30"
                ],
            ):
                d = date.fromisoformat(d_str)

                if (d.month, d.day) == target_md and gdd is not None:
                    hist_gdd.append(gdd)

            daily_moisture_map: dict[str, list[float]] = defaultdict(list)
            daily_soil_temp_map: dict[str, list[float]] = defaultdict(list)

            for t_str, m, st in zip(
                hist["hourly"]["time"],
                hist["hourly"]["soil_moisture_9_27cm"],
                hist["hourly"]["soil_temperature_6cm"],
            ):
                day_str = t_str[:10]
                d = date.fromisoformat(day_str)

                if (d.month, d.day) == target_md:
                    if m is not None:
                        daily_moisture_map[day_str].append(m)

                    if st is not None:
                        daily_soil_temp_map[day_str].append(st)

            hist_moisture = [
                statistics.mean(vals)
                for vals in daily_moisture_map.values()
            ]

            hist_soil_temp = [
                statistics.mean(vals)
                for vals in daily_soil_temp_map.values()
            ]

        except Exception as e:
            print(f"[Harvest Historical Error] {e}")
            return "Unavailable"


        def vs_normal(today_val: float, hist_vals: list[float]) -> int:
            """
            Returns:
                +1 = above normal
                 0 = normal
                -1 = below normal
            """

            if len(hist_vals) < 5:
                return 0

            mean = statistics.mean(hist_vals)

            stdev = (
                statistics.stdev(hist_vals)
                if len(hist_vals) > 1
                else 1.0
            )

            if today_val > mean + stdev:
                return 1

            elif today_val < mean - stdev:
                return -1

            return 0

        gdd_score = vs_normal(gdd_today, hist_gdd)
        moisture_score = vs_normal(
            soil_moisture_today,
            hist_moisture,
        )
        soil_temp_score = vs_normal(
            soil_temp_today,
            hist_soil_temp,
        )

        if soil_temp_today < 5.0:
            return "Poor — Soil Too Cold"

        if moisture_score == 1 and gdd_score <= 0:
            return "Poor — Waterlogged"

        total = (
            gdd_score
            + moisture_score
            + soil_temp_score
        )

        if total >= 2:
            return "Favorable"
        elif total == 1:
            return "Good"
        elif total == 0:
            return "Normal"
        elif total == -1:
            return "Below Normal"
        else:
            return "Poor"