import os
import re
import yaml

def __extract_functions(file_content):
    
    # Regular expression to match C function definitions
    REGULAR_EXPRESSION_C = r"(^\w[\w\s\*]+)\s+(\w+)\s*\(([^)]*)\)\s*(\{[^{}]*\})"
    REGULAR_EXPRESSION_ANNOTATION = r"(^\@[A-Z]\w+){1}(\(.+\))*"
    
    
    function_pattern = re.compile(REGULAR_EXPRESSION_C, re.MULTILINE)
    function_matches = function_pattern.finditer(file_content)

    annotation_pattern = re.compile(REGULAR_EXPRESSION_ANNOTATION, re.MULTILINE)

    functions = []
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
        func_content = match.group(4).strip()
        
        # function_contents.append(
        #     f"{func_return_type} {func_name}({func_args}) {match.group(4)}"
        # )
        functions.append({
            "name": func_name,
            "return_type": func_return_type,
            "args": func_args,
            "annotations": annotations,
            "content": func_content
        })

    return functions

def create_independent_files(functions, output_dir):
    
    for fun in functions:
        
        filename = f"{fun['name']}.c"
        with open(output_dir + filename, "w") as f:
            
            # Write the code
            f.write(fun["code"])
            
def extract_functions_from_file(input_file):
    
    with open(input_file, "r") as file:
        file_content = file.read()
        
    functions = __extract_functions(file_content)
    return functions

def save_functions_to_yaml(functions, output_file):
    
    with open(output_file, "w") as file:
        yaml.dump(functions, file, sort_keys=False)
