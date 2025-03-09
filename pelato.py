import argparse
import src
import src.utils as ut
import time

def main():
    
    parser = argparse.ArgumentParser(
        description="Generate, build and deploy WASM components written in go"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command list")

    parser_generate = subparsers.add_parser("gen", help="Generate Go code")
    parser_generate.add_argument("dir", type=str, help="Project directory")

    parser_build = subparsers.add_parser("build", help="Build WASM component")
    parser_build.add_argument("dir", type=str, help="Project directory")

    parser_deploy = subparsers.add_parser("deploy", help="Deploy WASM components")
    parser_deploy.add_argument("dir", type=str, help="Project directory")
    
    parser_remove = subparsers.add_parser("remove", help="Remove deployed WASM components")
    parser_remove.add_argument("dir", type=str, help="Project directory")
    
    parser_all = subparsers.add_parser("brush", help="Starts the pipeline: gen -> build -> deploy")
    parser_all.add_argument("dir", type=str, help="Project directory")

    # Parsing degli argomenti
    args = parser.parse_args()
    
    # Setup Pelato
    pelato = src.Pelato()
    
    if pelato.metrics_enabled:
        pelato.metrics = {}
        start_time = time.time()

    # Esecuzione del comando specificato
    if args.command == "gen":
        pelato.generate(args.dir)
    elif args.command == "build":
        pelato.build(args.dir)
    elif args.command == "deploy":
        pelato.deploy(args.dir)
    elif args.command == "remove":
        pelato.remove(args.dir)
    elif args.command == "brush":
        pelato.all(args.dir)
    else:
        parser.print_help()
        return

    if pelato.metrics_enabled:
        end_time = time.time()
        pelato.metrics['time_total'] = '%.3f'%(end_time - start_time)
        
        full_metrics = ut.load_metrics(args.dir)
        full_metrics['runs'].append(pelato.metrics)
        ut.dump_metrics(full_metrics, args.dir)
        
if __name__ == "__main__":
    main()
