with import <nixpkgs> {};

let
  packages = python-packages: with python-packages; [
    twine
    wheel
  ];
in
stdenv.mkDerivation {
  name = "pyutils";
  buildInputs = [
    (python3.withPackages packages)
    pipenv
  ];

  shellHook = "
    export SOURCE_DATE_EPOCH=315532800 # 1980
  ";
}
