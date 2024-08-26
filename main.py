import src.task_splitter.code_processor as splitter
import src.task_splitter.code_generator as generator

input_file = "source-code/tasks.c"  # Replace this with your actual file name
output_dir = "build/"

functions = splitter.extract_functions_from_file(input_file)
print(f"Found {len(functions)} functions in the file.")

generator.build_code_from_functions(functions)
print("Code has been generated for each function.")

splitter.create_independent_files(functions, output_dir)
print("Functions have been split into separate files with their own main functions.")

splitter.save_functions_to_yaml(functions, output_dir + "functions.yaml")