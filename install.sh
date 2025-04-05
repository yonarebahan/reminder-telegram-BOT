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

echo "📦 Membuat virtual environment..."
python3 -m venv venv

echo "✅ Mengaktifkan virtual environment..."
source venv/bin/activate

echo "📦 Menginstall dependencies..."
pip install -r requirements.txt

if [ -f ".env" ]; then
    echo "⚠️  File .env sudah ada, tidak disalin ulang."
else
    if [ -f ".env.example" ]; then
        echo "📄 Menyalin .env.example ke .env..."
        cp .env.example .env
    else
        echo "❌ Tidak menemukan file .env.example. Silakan buat manual."
    fi
fi

echo ""
echo "✅ Instalasi selesai!"
