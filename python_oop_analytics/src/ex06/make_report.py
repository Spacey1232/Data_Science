import config
import urllib.error
from analytics import Research


def main():
    reader = Research(config.data_path)

    try:
        data = reader.file_reader()
        analytics = Research.Analytics(data)

        count_orel, count_res = analytics.counts()

        fraction_orel, fraction_res = analytics.fractions(
            count_orel,
            count_res
        )

        predictions = analytics.predict_random(config.num_of_steps)

        prediction_calculation = Research.Calculations(predictions)
        predicted_orel, predicted_res = prediction_calculation.counts()

        total_observations = count_orel + count_res

        report_text = config.report_template.format(
            total_observations=total_observations,
            count_res=count_res,
            count_orel=count_orel,
            fraction_res=fraction_res,
            fraction_orel=fraction_orel,
            num_of_steps=config.num_of_steps,
            predicted_res=predicted_res,
            predicted_orel=predicted_orel
        )

        analytics.save_file(report_text, "report", "txt")

    except (ValueError, OSError, KeyError):
        reader.send_message(
            "The report hasn't been created due to an error."
        )
        raise

    else:
        reader.send_message(
            "The report has been successfully created"
        )


if __name__ == "__main__":
    try:
        main()
    except (
        ValueError,
        OSError,
        KeyError,
        urllib.error.URLError
    ) as error:
        print(f"Ошибка: {error}")
        raise SystemExit(1)