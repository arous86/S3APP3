#!/bin/sh

echo "Commandes simplifiées disponibles:"
echo "  call"
echo "  call_std"
echo ""
echo "Pour des commandes plus complexes, voir aussi /usr/local/bin/listTodo.py: "
echo "  (accessible directement par la commande call_std)"
python3 /usr/local/bin/callTodo.py --help
