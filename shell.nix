{ pkgs ? import <nixpkgs> { } }:

let
  python = pkgs.python313.withPackages (ps: with ps; [
    tkinter
    simpleaudio
  ]);
in
pkgs.mkShell {
  packages = [ python ];
}
