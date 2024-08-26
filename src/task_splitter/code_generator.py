
import ast

def __get_include_from_annotation(libdeps):
    
    result = ""
    
    for lib in libdeps:
        result += f"#include <{lib}>\n"
        
    return result

def __get_main_function_from_function(fun):
    
    main_function = f"""
int main() {{
    
    {fun['name']}({', '.join(['0' for _ in fun['args'].split(',')])});
    return 0;
}}\n
    """
    return main_function

def get_code_from_function(fun):
    
    # Get the function content
    function_content = f"{fun['return_type']} {fun['name']}({fun['args']}) {fun['content']}"
    
    # Get the main function
    main_function = __get_main_function_from_function(fun)
    
    # Get the dependencies from the annotations
    libdeps = ""
    for ann in fun['annotations']:
        if ann['tag'] == "@LibDeps":
            libdeps= ast.literal_eval(ann['args'])
            break
    
    # Get the include statements
    include_statements = __get_include_from_annotation(libdeps=libdeps)
    
    return include_statements + '\n' + function_content + '\n' + main_function

def build_code_from_functions(functions):
    
    for fun in functions:
        fun["code"] = get_code_from_function(fun)
