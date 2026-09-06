from unittest.mock import patch

from app.models.cliente import Cliente


def test_gestao_clientes_retorna_pagina(client):
    response = client.get("/clientes")

    assert response.status_code == 200
    assert b"Clientes cadastrados" in response.data


def test_gestao_clientes_delega_para_service(client):
    clientes = [
        Cliente(
            id=1,
            tipo_pessoa="PF",
            nome_razao_social="Cliente Teste",
            email="cliente@exemplo.com",
            telefone="48999999999",
            ativo=True,
        ),
    ]

    with patch(
        "app.routes.cliente_web.ClienteService.listar_todos",
        return_value=clientes,
    ) as mock_listar:
        response = client.get("/clientes")

    assert response.status_code == 200
    mock_listar.assert_called_once_with()
    assert b"Cliente Teste" in response.data


def test_criar_cliente_redireciona_para_listagem(client):
    with patch(
        "app.routes.cliente_web.ClienteService.criar",
        return_value=Cliente(
            id=1,
            tipo_pessoa="PF",
            nome_razao_social="Cliente POST",
            email="cliente.post@example.com",
            telefone="48999999999",
            ativo=True,
        ),
    ) as mock_criar:
        response = client.post(
            "/clientes",
            data={
                "tipo_pessoa": "PF",
                "nome_razao_social": "Cliente POST",
                "email": "cliente.post@example.com",
                "telefone": "48999999999",
            },
        )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/clientes")
    mock_criar.assert_called_once()


def test_criar_cliente_rejeita_campos_obrigatorios_ausentes(client):
    response = client.post(
        "/clientes",
        data={
            "tipo_pessoa": "PF",
            "nome_razao_social": "",
            "email": "",
            "telefone": "",
        },
    )

    assert response.status_code == 400
    assert b"Preencha os campos obrigat" in response.data