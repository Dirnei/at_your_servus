#!/usr/bin/env sh
# Servus server pack: installs NeoForge on first run, then starts the server. Needs Java 25.
set -e
cd "$(dirname "$0")"
NEOFORGE_VERSION=26.1.2.122
if [ ! -f run.sh ]; then
    installer="neoforge-$NEOFORGE_VERSION-installer.jar"
    curl -fL -o "$installer" "https://maven.neoforged.net/releases/net/neoforged/neoforge/$NEOFORGE_VERSION/$installer"
    java -jar "$installer" --installServer
    rm -f "$installer" "$installer.log"
fi
if ! grep -qs "eula=true" eula.txt; then
    echo "Read https://aka.ms/MinecraftEULA and set eula=true in eula.txt, then start again."
    echo "eula=false" > eula.txt
    exit 1
fi
exec sh ./run.sh nogui
