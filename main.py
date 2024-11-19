import azure_functions.call_handler as call_handler
import azure_functions.data_processor as data_processor

def main():
    # Load input data
    input_file = "templates/input_template.xlsx"
    patient_data = data_processor.read_excel(input_file)

    # Process calls for each patient
    results = []
    for data in patient_data:
        result = call_handler.initiate_call(data)
        results.append(result)

    # Export results
    output_file = "templates/output_template.xlsx"
    data_processor.write_excel(results, output_file)

if __name__ == "__main__":
    main()
