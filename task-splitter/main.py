import os
import re
import yaml

def extract_functions(file_content):
    # Regular expression to match C function definitions
    function_pattern = re.compile(r"(^\w[\w\s\*]+)\s+(\w+)\s*\(([^)]*)\)\s*(\{[^{}]*\})", re.MULTILINE)
    function_matches = function_pattern.finditer(file_content)

    annotation_pattern = re.compile(r"(\@[A-Z]\w+){1}(\(.+\))*")

    functions = []
    function_contents = []
    positions = []

    for match in function_matches:
        positions.append(match.start())
        annotation_matches = annotation_pattern.finditer(file_content)        
        prev = 0
        
        if len(positions) > 1:
            prev = positions[-2]
        
        annotations = []
        
        for ann in annotation_matches:
            if ann.start() >= prev:
                
                if ann.start() > match.start():
                    break
                
                ann_tag = ann.group(1).strip()
                ann_arg = ann.group(2)
                
                if ann_arg is not None:
                    ann_arg = ann_arg.replace("(","[").replace(")","]")
                
                annotations.append(
                    {
                    "tag": ann_tag,
                    "args": ann_arg
                    }
                )
        
        
        func_return_type = match.group(1).strip()
        func_name = match.group(2)
        func_args = match.group(3).strip()
        
        function_contents.append(
            f"{func_return_type} {func_name}({func_args}) {match.group(4)}"
        )
        functions.append({
            "name": func_name,
            "return_type": func_return_type,
            "args": func_args,
            "annotations": annotations
        })


    return functions, function_contents

def create_independent_files(functions, function_contents, output_dir):
    for i, function in enumerate(functions):
        filename = f"{function['name']}.c"
        with open(output_dir + filename, "w") as f:
            # Write the original function
            f.write(function_contents[i])
            f.write("\n")
            
            # Add a main function to call the function
            main_function = f"""
            int main() {{
                // Assuming that the function has no return value, or you can modify it to handle return values.
                {function['name']}({', '.join(['0' for _ in function['args'].split(',')])});
                return 0;
            }}
            """
            f.write(main_function)

def split_functions_into_files(input_file, output_dir):
    with open(input_file, "r") as file:
        file_content = file.read()

    functions, function_contents = extract_functions(file_content)
    
    with open(output_dir + "config.yaml","w") as outfile:
        yaml.safe_dump(functions, outfile, default_style=None, default_flow_style=False, sort_keys=False)
    
    create_independent_files(functions, function_contents, output_dir)

if __name__ == "__main__":
    input_file = "src/tasks.c"  # Replace this with your actual file name
    output_dir = "build/"
    split_functions_into_files(input_file, output_dir)
    print("Functions have been split into separate files with their own main functions.")
