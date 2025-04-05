#!/bin/bash

clear
echo ""
echo "                      .^!!^."
echo "                  .:~7?7!7??7~:."
echo "               :^!77!~:..^^~7?J?!^."
echo "           .^!7??!^..  ..^^^^^~JJJJ7~:."
echo "           7?????: ...^!7?!^^^~JJJJJJJ?."
echo "           7?????:...^???J7^^^~JJJJJJJJ."
echo "           7?????:...^??7?7^^^~JJJJJJJ?."
echo "           7?????:...^~:.^~^^^~JJJJJJJ?."
echo "           7?????:.. .:^!7!~^^~7?JJJJJ?."
echo "           7?????:.:~JGP5YJJ?7!^^~7?JJ?."
echo "           7?7?JY??JJ5BBBBG5YJJ?7!~7JJ?."
echo "           7Y5GBBYJJJ5BBBBBBBGP5Y5PGP5J."
echo "           ^?PBBBP555PBBBBBBBBBBBB#BPJ~"
echo "              :!YGB#BBBBBBBBBBBBGY7^"
echo "                 .~?5BBBBBBBBPJ~."
echo "                     :!YGGY7:"
echo "                        .."
echo ""
echo " 🚀 join channel Airdrop Sambil Rebahan : https://t.me/kingfeeder "
echo ""
echo ""
echo "🚀 Menginstall dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip

echo ""
echo "📦 Menginstall python packages..."
pip3 install -r requirements.txt

echo ""
echo "📁 Membuat file .env jika belum ada..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env berhasil dibuat dari .env.example"
else
    echo "ℹ️  File .env sudah ada, dilewati."
fi

echo ""
echo "✅ Instalasi selesai!"
echo "👉 Jalankan bot
