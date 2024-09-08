#!/bin/bash

function assert_output_contains() {
    expected_substring=$1
    command=$2
    shift 2
    args="$@"

    output=$($command $args)

    if [[ $output == *$expected_substring* ]]; then
        echo -e "\e[32mTest passed:\e[0m Expected '$expected_substring' in output of '$command $args'"
    else
        echo -e "\e[31mTest failed:\e[0m Did not find '$expected_substring' in output of '$command $args' instead i find '$output'"
        exit 1
    fi
}

rm estado.json

assert_output_contains "Exito!" python3 main.py alta 391238934 clave 40840323 123 ricardo 5000 2
assert_output_contains "usuario ya existe" python3 main.py alta 391238934 clave 40840323 123 ricardo 2 2
assert_output_contains "credenciales de admin invalidas" python3 main.py alta 391238934 hola 40840323 123 ricardo 2 2

assert_output_contains "Exito!" python3 main.py carga 391238934 clave 100
assert_output_contains "Exito!" python3 main.py carga 391238934 clave 50

assert_output_contains "Clave invalida" python3 main.py clave 40840323 450 100
assert_output_contains "Clave debil" python3 main.py clave 40840323 123 100
assert_output_contains "Exito!" python3 main.py clave 40840323 123 Pingora82 
assert_output_contains "Limite de cambio de clave alcanzado" python3 main.py clave 40840323 Pingora82 Pingora81 

assert_output_contains "Saldo insuficiente en el cajero" python3 main.py extraccion 40840323 Pingora82 180 
assert_output_contains "Limite de monto alcanzado" python3 main.py extraccion 40840323 Pingora82 6000 
assert_output_contains "5000" python3 main.py saldo 40840323 Pingora82 
assert_output_contains "Exito!" python3 main.py extraccion 40840323 Pingora82 100 


assert_output_contains "4900" python3 main.py saldo 40840323 Pingora82 

assert_output_contains "[]" python3 main.py movimientos 391238934 clave 40840323 2023-01-03 2023-02-04 
# assert_output_contains "[]" python3 main.py movimientos 391238934 clave 40840323 2023-01-03 2029-02-04 



assert_output_contains "Exito!" python3 main.py carga 391238934 clave 10000
assert_output_contains "Exito!" python3 main.py extraccion 40840323 Pingora82 100 
assert_output_contains "Exito!" python3 main.py extraccion 40840323 Pingora82 100 
assert_output_contains "Limite diario de operaciones alcanzado" python3 main.py extraccion 40840323 Pingora82 100 
