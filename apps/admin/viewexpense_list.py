from dash import dash, html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import dash 
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go

from app import app
from apps import commonmodules as cm
from apps import dbconnect as db
from datetime import datetime

layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("Expense Types List"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                        dbc.Button("Add Expense Type", color="primary"),
                                        href="/expense_list/add_expensetype",
                                        style={"text-align": "right"}
                                    ),
                                    width={"size": 8}  
                                ),
                            ],
                        ),

                        html.Div(
                            id='expensetype_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto', 
                                'overflowY': 'auto',   
                                'maxHeight': '800px',
                            }
                        ),
                        
                        # Confirmation Modal: asks the user to confirm the removal
                        # dbc.Modal(
                        #     [
                        #         dbc.ModalHeader(html.H3("Confirm Choice of Removal"), className="bg-primary"),
                        #         dbc.ModalBody(html.H5("Are you sure you want to remove this expense type?")),
                        #         dbc.ModalFooter(
                        #             [
                        #                 dbc.Button("Cancel", id="confirm-modal-cancel", color="warning"),
                        #                 dbc.Button("Confirm", id="confirm-modal-confirm", color="danger"),
                        #             ]
                        #         ),
                        #     ],
                        #     id="confirm-modal",
                        #     centered=True,
                        #     is_open=False,
                        #     backdrop=True
                        # ),

                        # Settings Modal: To adjust budget and removal
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Edit Expense Type"), className="bg-primary"),
                                dbc.ModalBody([
                                    html.Div(id="allex_name"),
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Label(
                                                ["Main Expense Budget Allocation (₱)", 
                                                html.Span("*", style={"color": "#F8B237"})],
                                            ),
                                            width="auto",
                                            align="end"
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                id="edit_main_budget",
                                                placeholder="0000.00",
                                                type="text",
                                            ),
                                            width=4
                                        )
                                    ],
                                    style={'marginTop': '20px'}),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Checklist(
                                            id="expensetype_removerecord",
                                            options= [
                                                {
                                                    'label': "Mark for Deletion",
                                                    'value': 1
                                                }
                                            ],
                                            style={'fontWeight':'bold'},
                                        )
                                    ])
                                ]),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id="confirm-modal-cancel", color="warning"),
                                        dbc.Button("Confirm", id="confirm-modal-confirm", color="danger"),
                                    ]
                                )
                            ],
                            id="confirm-modal",
                            centered=True,
                            is_open=False,
                            backdrop=True
                        ),

                        # Final Modal: notifies the user that the removal is complete
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Edited Successfully"), className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Expense type has been successfully edited."))
                            ],
                            id="final-modal",
                            centered=True,
                            is_open=False,
                        ),
                    ],
                    width=9,
                    style={'marginLeft': '15px'},
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        ),
    ]
)

# Generates the expense types table.
@app.callback(
    Output('expensetype_list', 'children'),
    [Input('url', 'pathname')]
)
def expensetype_list(pathname):
    if pathname == '/expense_list':
        sql = """
            SELECT 
                me.main_expense_id AS "ID",
                me.main_expense_shortname AS "Main Expense",
                '' AS "Sub Expense",
                me.main_expense_budget AS "Budget (₱)",
                'main' AS "Type"
            FROM adminteam.main_expenses me
            WHERE me.main_expense_del_ind = FALSE

            UNION ALL

            SELECT 
                se.sub_expense_id AS "ID",
                me.main_expense_shortname AS "Main Expense",
                se.sub_expense_name AS "Sub Expense",
                NULL AS "Budget (₱)",
                'sub' AS "Type"
            FROM adminteam.sub_expenses se
            JOIN adminteam.main_expenses me ON se.main_expense_id = me.main_expense_id
            WHERE se.sub_expense_del_ind = FALSE

            ORDER BY "Main Expense", "Type", "Sub Expense"
        """
        cols = ["ID", "Main Expense", "Sub Expense", "Budget (₱)", "Type"]

        df = db.querydatafromdatabase(sql, [], cols)

        if df.shape[0] > 0:
            df["Action"] = df.apply(
                lambda row: html.Div(
                    dbc.Button(
                        'Edit',
                        id={'type': 'edit-button', 'index': f"{row['Type']}_{row['ID']}"},
                        size='sm',
                        color='primary'
                    ),
                    style={'text-align': 'center'}
                ),
                axis=1
            )

            df = df[["Main Expense", "Sub Expense", "Budget (₱)", "Action"]]

            table_rows = []
            for _, row in df.iterrows():
                row_color = "#e9ecef" if row["Sub Expense"] == "" else "white"
                table_rows.append(html.Tr([
                    html.Td(row["Main Expense"]),
                    html.Td(row["Sub Expense"]),
                    html.Td(row["Budget (₱)"]),
                    html.Td(row["Action"]),
                ], style={"background-color": row_color}))

            return [dbc.Table(
                [html.Thead(html.Tr([html.Th(col) for col in df.columns]))] +
                [html.Tbody(table_rows)]
            )]
        else:
            return [html.Div("No expense types listed")]
    else:
        raise PreventUpdate

# Callback to process edits to expense type
@app.callback(
    [
        Output('expensetype_list', 'children', allow_duplicate=True),
        Output("confirm-modal", "is_open"),
        Output("final-modal", "is_open")
    ],
    [
        Input({'type': 'edit-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
        Input("confirm-modal-confirm", "n_clicks"),
        Input("confirm-modal-cancel", "n_clicks"),
    ],
    [
        State({'type': 'edit-button', 'index': dash.dependencies.ALL}, 'id'),
        State("edit_main_budget", 'value'),
        State("expensetype_removerecord", 'value'),
        State("confirm-modal", "is_open"),
    ],
    prevent_initial_call=True
)
def process_removal(n_clicks_list, confirm_btn, cancel_btn, button_id_list, budgetval, removerecord, confirmationmodal):
    
    output_list = no_update
    confirm_modal = False
    final_modal = False
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    
    event_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if not n_clicks_list or not any(n_clicks_list):
        raise PreventUpdate

    # Use a substring check instead of an exact string match.
    if "edit-button" in event_id:
        confirm_modal = True
        final_modal = False

    elif event_id == "confirm-modal-confirm" and confirm_btn:
        if confirmationmodal:
            output_list = []
            for n_clicks, button_id in zip(n_clicks_list, button_id_list):
                if n_clicks:
                    index_str = button_id['index']
                    exp_type, expensetype_id = index_str.split('_', 1)
                    if exp_type == 'main':
                        update_expense_sql = """
                            UPDATE adminteam.main_expenses
                            SET 
                                main_expense_budget = %s,
                                main_expense_del_ind = %s
                            WHERE main_expense_id = %s
                        """
                        vals = [float(budgetval), bool(removerecord), int(expensetype_id)]
                    else:
                        update_expense_sql = """
                            UPDATE adminteam.sub_expenses
                            SET 
                                sub_expense_del_ind = %s
                            WHERE sub_expense_id = %s
                        """
                        vals = [bool(removerecord), int(expensetype_id)]

                    db.modifydatabase(update_expense_sql, vals)
                    output_list.append(expensetype_list('/expense_list')[0])
                    final_modal = True
                    confirm_modal = False

    elif event_id == "confirm-modal-cancel" and cancel_btn:
        if confirmationmodal:
            confirm_modal = False

    return [output_list, confirm_modal, final_modal]

# displaying the choices for the text area
@app.callback(
    [Output('allex_name', 'children'),
     Output('edit_main_budget', 'value'),
     Output('edit_main_budget', 'disabled')],
    Input({'type': 'edit-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    [State({'type': 'edit-button', 'index': dash.dependencies.ALL}, 'id'),
     State("confirm-modal", "is_open")]
)
def update_textarea_on_option_change(n_clicks_list, button_id_list, confirm_modal):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate    
    event_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if not n_clicks_list or not any(n_clicks_list):
        raise PreventUpdate
    else:
        for n_clicks, button_id in zip(n_clicks_list, button_id_list):
            index_str = f'\"{button_id['index']}\"'
            if n_clicks and (index_str in event_id):              
                index_str = index_str.replace("\"", "")
                exp_type, expensetype_id = index_str.split('_', 1)
                if exp_type == 'main':
                    sql = """
                        SELECT main_expense_name, main_expense_budget
                        FROM adminteam.main_expenses
                        WHERE main_expense_id = %s
                    """
                    values = [expensetype_id]
                    cols = ['Name', 'Budget']
                    df = db.querydatafromdatabase(sql, values, cols)
                    namestr = html.H5(df['Name'][0])
                    if not df.empty:
                        return [namestr, df['Budget'][0], False]
                    else:
                        return [namestr, "", False]
                else:
                    sql = """
                        SELECT sub_expense_name
                        FROM adminteam.sub_expenses
                        WHERE sub_expense_id = %s
                    """
                    values = [expensetype_id]
                    cols = ['Name']
                    df = db.querydatafromdatabase(sql, values, cols)
                    namestr = html.H5(df['Name'][0])
                    return [namestr, "", True]
    return ""

# # Callback to process confirmation modals
# @app.callback(
#     [
#         Output('expensetype_list', 'children', allow_duplicate=True),
#         Output("confirm-modal", "is_open"),
#         Output("final-modal", "is_open")
#     ],
#     [
#         Input({'type': 'remove-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
#         Input("confirm-modal-confirm", "n_clicks"),
#         Input("confirm-modal-cancel", "n_clicks"),
#     ],
#     [
#         State({'type': 'remove-button', 'index': dash.dependencies.ALL}, 'id'),
#         State("confirm-modal", "is_open"),
#     ],
#     prevent_initial_call=True
# )
# def process_removal(n_clicks_list, confirm_btn, cancel_btn, button_id_list, confirmationmodal):
    
#     output_list = no_update
#     confirm_modal = False
#     final_modal = False
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         raise PreventUpdate
    
#     event_id = ctx.triggered[0]['prop_id'].split('.')[0]

#     if not n_clicks_list or not any(n_clicks_list):
#         raise PreventUpdate

#     # Use a substring check instead of an exact string match.
#     if "remove-button" in event_id:
#         confirm_modal = True
#         final_modal = False

#     elif event_id == "confirm-modal-confirm" and confirm_btn:
#         if confirmationmodal:
#             output_list = []
#             for n_clicks, button_id in zip(n_clicks_list, button_id_list):
#                 if n_clicks:
#                     index_str = button_id['index']
#                     exp_type, expensetype_id = index_str.split('_', 1)
#                     if exp_type == 'main':
#                         update_expense_sql = """
#                             UPDATE adminteam.main_expenses
#                             SET main_expense_del_ind = TRUE
#                             WHERE main_expense_id = %s
#                         """
#                     else:
#                         update_expense_sql = """
#                             UPDATE adminteam.sub_expenses
#                             SET sub_expense_del_ind = TRUE
#                             WHERE sub_expense_id = %s
#                         """
#                     db.modifydatabase(update_expense_sql, [int(expensetype_id)])
#                     output_list.append(expensetype_list('/expense_list')[0])
#                     final_modal = True
#                     confirm_modal = False

#     elif event_id == "confirm-modal-cancel" and cancel_btn:
#         if confirmationmodal:
#             confirm_modal = False

#     return [output_list, confirm_modal, final_modal]

