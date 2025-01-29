import argparse
import src

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
    
    parser_all = subparsers.add_parser("brush", help="Everything above")
    parser_all.add_argument("dir", type=str, help="Project directory")

    # Parsing degli argomenti
    args = parser.parse_args()
    
    # Setup Pelato
    pelato = src.Pelato()

    # Esecuzione del comando specificato
    if args.command == "gen":
        pelato.generate(args.dir)
    elif args.command == "build":
        pelato.build(args.dir)
    elif args.command == "deploy":
        pelato.deploy(args.dir)
    elif args.command == "brush":
        pelato.all(args.dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
