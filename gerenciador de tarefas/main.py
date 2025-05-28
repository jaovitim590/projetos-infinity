import flet as ft

def main(page: ft.Page):
    tarefas = []

    page.title = "gerenciador de tarefas"

    nome_tarefa = ft.TextField(label="Nome da tarefa", width=500)
    prioridade = ft.Dropdown(
        label="Prioridade",
        options=[
            ft.dropdown.Option("baixa"),
            ft.dropdown.Option("média"),
            ft.dropdown.Option("alta"),
        ],
        width=200
    )
    descricao = ft.TextField(label="Descrição", width=500)

    def criar_tarefa(e):
        tarefa = {
            "nome": nome_tarefa.value,
            "prioridade": prioridade.value,
            "descricao": descricao.value,
            "concluido": False
        }
        tarefas.append(tarefa)
        nome_tarefa.value = ""
        prioridade.value = None
        descricao.value = ""
        page.update()
        page.go("/")

    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Text("Menu inicial", size=20, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Adicionar tarefa", on_click=lambda _: page.go("/adicionar_tarefa"), width=200),
                        ft.ElevatedButton("Ver tarefas", on_click=lambda _: page.go("/ver_tarefas"), width=200),
                        ft.ElevatedButton("Concluir tarefas", on_click=lambda _: page.go("/concluir"), width=200)
                    ]
                )
            )

        elif page.route == "/adicionar_tarefa":
            page.views.append(
                ft.View(
                    "/adicionar_tarefa",
                    [
                        ft.Text("Preencha as informações para adicionar:", size=20, weight=ft.FontWeight.BOLD),
                        nome_tarefa,
                        prioridade,
                        descricao,
                        ft.ElevatedButton("Salvar", on_click=criar_tarefa, width=200),
                        ft.Container(
                            content=ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/"), width=150, height=75),
                            alignment=ft.alignment.bottom_center,
                            expand=True
                        )
                    ]
                )
            )

        elif page.route == "/ver_tarefas":
            conteudo_tarefas = [
                ft.Text("Tarefas existentes:", size=20, weight=ft.FontWeight.BOLD),
            ]
            if not tarefas:
                conteudo_tarefas.append(ft.Text("NENHUMA TAREFA CRIADA!", size=25, color=ft.Colors.RED))
            else:
                for t in tarefas:
                    status = "✅ Concluído" if t["concluido"] else "❌ Não concluído"
                    conteudo_tarefas.append(
                        ft.Card(
                            content=ft.ListTile(
                                title=ft.Text(f"{t['nome']} - Prioridade: {t['prioridade']}"),
                                subtitle=ft.Text(f"{t['descricao']}\nStatus: {status}"),
                            )
                        )
                    )
            conteudo_tarefas.append(
                ft.Container(
                    content=ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/"), width=150, height=75),
                    alignment=ft.alignment.bottom_center,
                    expand=True
                )
            )
            page.views.append(ft.View("/ver_tarefas", conteudo_tarefas))

        elif page.route == "/concluir":
            conteudo_tarefas = [
                ft.Text("Selecione uma tarefa para concluir:", size=20, weight=ft.FontWeight.BOLD),
            ]

            tarefas_pendentes = [t for t in tarefas if not t["concluido"]]

            if not tarefas_pendentes:
                conteudo_tarefas.append(ft.Text("NENHUMA TAREFA PENDENTE!", size=25, color=ft.Colors.RED))
            else:
                dropdown_tarefas = ft.Dropdown(
                    label="Tarefas",
                    options=[ft.dropdown.Option(t["nome"]) for t in tarefas_pendentes],
                    width=300
                )

                def concluir_tarefa(e):
                    for t in tarefas:
                        if t["nome"] == dropdown_tarefas.value:
                            t["concluido"] = True
                            break
                    page.go("/ver_tarefas")

                conteudo_tarefas.extend([
                    dropdown_tarefas,
                    ft.ElevatedButton("Concluir tarefa", on_click=concluir_tarefa, width=200)
                ])

            conteudo_tarefas.append(
                ft.Container(
                    content=ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/"), width=150, height=75),
                    alignment=ft.alignment.bottom_center,
                    expand=True
                )
            )
            page.views.append(ft.View("/concluir", conteudo_tarefas))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(main)
