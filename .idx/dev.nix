# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.nodejs_20
    pkgs.nodePackages.npm
    pkgs.docker-compose
  ];

  # Sets environment variables in the workspace
  env = {
    # Sets the port for the Next.js preview
    PORT = "3000";
    # DRY_RUN mode for backend
    DRY_RUN = "true";
  };

  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-python.python"
      "esbenp.prettier-vscode"
    ];

    # Enable previews
    previews = {
      enable = true;
      previews = {
        web = {
          # Example: run the frontend
          command = ["npm" "run" "dev" "--prefix" "frontend" "--" "--port" "$PORT" "--hostname" "0.0.0.0"];
          manager = "web";
        };
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        # Install backend dependencies
        install-backend = "pip install -r backend/requirements.txt";
        # Install frontend dependencies
        install-frontend = "cd frontend && npm install";
      };
      # Runs when the workspace is (re)started
      onStart = {
        # Ensure dependencies are up to date
        update-deps = "pip install -r backend/requirements.txt && cd frontend && npm install";
      };
    };
  };
}
