import azure_functions.call_handler as call_handler
import azure_functions.data_processor as data_processor
import logging

def main():
    try:
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Load input data
        input_file = "templates/input_template.xlsx"
        logger.info(f"Reading input data from {input_file}")
        patient_data = data_processor.read_excel(input_file)

        if not patient_data:
            logger.error("No patient data found in input file")
            return

        # Process calls for each patient
        results = []
        for data in patient_data:
            try:
                result = call_handler.initiate_call(data)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing patient {data.get('id', 'unknown')}: {str(e)}")
                results.append({
                    "patient_id": data.get('id', 'unknown'),
                    "call_status": "Failed",
                    "error": str(e)
                })

        # Export results
        output_file = "templates/output_template.xlsx"
        logger.info(f"Writing results to {output_file}")
        data_processor.write_excel(results, output_file)

    except Exception as e:
        logger.error(f"Main process failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
