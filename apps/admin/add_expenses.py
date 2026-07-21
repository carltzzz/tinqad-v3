import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, no_update
from dash import callback_context

import dash

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db 

import datetime
import locale
import re

from urllib.parse import urlparse, parse_qs


form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                       "Date ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='exp_date',
                        date=str(pd.to_datetime("today").date()),
                        className='SingleDatePicker',
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Payee ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='exp_payee', placeholder="First Name Last Name"),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Expense Main Type ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='main_expense_id',
                        options=[]
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Expense Sub Type ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='sub_expense_id',
                        options=[]
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Particulars ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                   dbc.Textarea(
                        id='exp_particulars', 
                        placeholder="Enter particulars"),
                   width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Amount ",
                        html.Span("*", style={"color": "#F8B237"}) 
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='exp_amount', placeholder="0,000.00"),
                    width=6,
                ),
                dbc.Col(
                    html.Div(id='amount-copy', style={"color": "#C4BDBD"}),
                    width=2,
                )
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    "Funding Source",
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='exp_funding_source', placeholder="Enter funding source"),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Status ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='exp_status',
                        options=[ 
                            {"label": "Approved", "value": 1},
                            {"label": "Pending", "value": 2},
                            {"label": "Denied", "value": 3},
                        ]
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
            style={'display': 'none'},
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "BUR No. ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='exp_bur_no', placeholder="0000-00-00000"),
                    width=6,
                ),
                dbc.Col(
                    html.Div(id='bur-no-copy', style={"color": "#C4BDBD"}),
                    width=2,
                )
            ],
            className="mb-3",
        ),
 
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Submitted by ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],  
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id = 'exp_submitted_by'),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Label(
                    "Receipt Link",
                    width=4,
                ),
                dbc.Col(
                    dbc.Input(
                        id="exp_receipt",
                        type="url",
                        placeholder="Paste Google Drive link here",
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        html.Br(),
    ],
    className="g-2",
)


#sub expense dropdown
@app.callback(
    Output('sub_expense_id', 'options'),
    Input('main_expense_id', 'value')
)
def update_subexpenses_options(selected_main_expense):
    if selected_main_expense is None:
        return []  # Return empty options if no main expense is selected
    
    try:
        # Query to fetch sub-expenses based on the selected main expense
        sql = """
        SELECT sub_expense_name as label, sub_expense_id as value
        FROM adminteam.sub_expenses
        WHERE main_expense_id = %s
        """
        values = [selected_main_expense]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        sub_expense_options = df.to_dict('records')
        return sub_expense_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 

#amount
locale.setlocale(locale.LC_ALL, '')

@app.callback(
    Output('amount-copy', 'children'),
    Input('exp_amount', 'value')
)
def update_amount_copy(value):
    if value is None:
        return None   

    try: 
        float_value = float(str(value).replace(',', ''))
        # Format the float value with commas and two decimal places
        formatted_value = locale.format_string("%0.2f", float_value, grouping=True)
        return formatted_value
    except (ValueError, TypeError): 
        return None

#bur
@app.callback(
    Output('bur-no-copy', 'children'),
    Input('exp_bur_no', 'value')
)
def update_bur_no_copy(value):
    if value:
        # Remove any non-digit characters
        cleaned_value = re.sub(r'\D', '', value)
        # Format the cleaned value as ####-##-#####
        formatted_value = '-'.join([cleaned_value[:4], cleaned_value[4:6], cleaned_value[6:]])
        return formatted_value
    else:
        return ''

 
layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                [
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H1(id="expenses_header"),
                                    style={"marginRight": "auto"}
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Edit", color="warning",
                                        id='addexpense_toggle_edit',
                                        n_clicks=0,
                                        style={'display': 'none'}
                                    ),
                                    width="auto",
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Back",
                                        color="success",
                                        href="/record_expenses"
                                    ),
                                    width="auto",
                                    id="expenses_back_btn_div",
                                )
                            ],
                            align="center"
                        ),
                        className="mb-4"
                    ),
                    html.Hr(),
                    html.Div(  
                            [
                                dcc.Store(id='recordexpenses_toload', storage_type='memory', data=0),
                                dcc.Store(id='addexpense_edit_mode', storage_type='memory', data=0),
                            ]
                        ),
                    dbc.Alert(id='recordexpenses_alert', is_open=False), # For feedback purpose
                    form, 
                    html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='recordexpenses_removerecord',
                                            options=[
                                                {
                                                    'label': "Mark for Deletion",
                                                    'value': 1
                                                }
                                            ], 
                                            style={'fontWeight':'bold'},
                                        ),
                                        width=5,
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='recordexpenses_removerecord_div'
                        ),

                        html.Br(),
                        html.Div(
                            dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="recordexpenses_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="recordexpenses_cancel_button", n_clicks=0, href="/record_expenses"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-3",
                            justify="end",
                            ),
                        id='recordexpenses_buttons_div',
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(html.H5(id='confirmation_modal_message')),
                                dbc.ModalFooter(
                                        [
                                            dbc.Button("Cancel", id="confirmation_modal_cancel", color="warning"),
                                            dbc.Button("Confirm", id="confirmation_modal_confirm", color="success"),
                                        ], 
                                )
                                
                            ],
                            centered=True,
                            id='confirmation_modal',
                            backdrop=True,   
                            className="modal-success"    
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3(id="final_modal_header"), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(html.H5("Click Proceed to continue.")),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed",
                                        href="/record_expenses",
                                        color="success", 
                                    ),
                                ),
                            ],
                            centered=True,
                            id='final_modal',
                            backdrop='static',
                            keyboard=False,
                        ),  
                ],
                width=8,
                style={"marginLeft": "15px"},
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        ), 
    ]
)


#main expense dropdown
@app.callback(
    [
        Output('expenses_header', 'children'),
        Output('main_expense_id', 'options'),
        Output('recordexpenses_toload', 'data'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)

def populate_mainexpenses_dropdown(pathname, search):
    # Check if the pathname matches if necessary
    if pathname == '/record_expenses/add_expense':
        sql = """
            SELECT main_expense_name as label,  main_expense_id  as value
            FROM adminteam.main_expenses

            WHERE main_expense_del_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        main_expense_types = df.to_dict('records')
         
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        if create_mode == 'add':
            header = 'Add Expense Record'
            to_load = 0
        elif create_mode == 'edit':
            header = 'Edit Expense Record'
            to_load = 1
        elif create_mode == 'view':
            header = 'View Expense Record'
            to_load = 1
    else:
        raise PreventUpdate
    return [header, main_expense_types, to_load]



@app.callback(
    [
        # Check if all fields are filled
        Output('recordexpenses_alert', 'is_open'),
        Output('recordexpenses_alert', 'color'),
        Output('recordexpenses_alert', 'children'),
        Output('exp_date', 'className'),
        Output('exp_payee', 'className'),
        Output('main_expense_id', 'className'),
        Output('sub_expense_id', 'className'),
        Output('exp_particulars', 'className'),
        Output('exp_amount', 'className'),
        Output('exp_status', 'className'),
        Output('exp_bur_no', 'className'),
        Output('exp_submitted_by', 'className'),
        # Open confirmation modal
        Output('confirmation_modal', 'is_open'), 
        Output('confirmation_modal_message', 'children'),
        # Button Colors Change When in Edit Mode
        Output("confirmation_modal_confirm", "color"),
        # Open success modal
        Output('final_modal', 'is_open'),
        Output('final_modal_header', 'children'),
    ],
    [
        Input('recordexpenses_save_button', 'n_clicks'),
        Input('confirmation_modal_confirm', 'n_clicks'),
        Input('confirmation_modal_cancel', 'n_clicks'),
    ], 
    [   
        State('recordexpenses_removerecord', 'value'),
        State('confirmation_modal', 'is_open'),
        State('exp_date', 'date'),
        State('exp_payee', 'value'),
        State('main_expense_id', 'value'),
        State('sub_expense_id', 'value'),
        State('exp_particulars', 'value'),
        State('exp_amount', 'value'),
        State('exp_status', 'value'),
        State('exp_bur_no', 'value'),
        State('exp_submitted_by', 'value'),
        State('exp_funding_source', 'value'),
        State('exp_receipt', 'value'),
        State('url', 'search'),
        State('addexpense_edit_mode', 'data'),
    ]
)
def save_expense(submitbtn, confirmbtn, cancelbtn, removerecord,confirmationmodal,
                 exp_date, exp_payee, main_expense_id, sub_expense_id,
                 exp_particulars, exp_amount, exp_status, 
                 exp_bur_no, exp_submitted_by, exp_funding_source,
                 exp_receipt_link, search, edit_mode):

    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    # Prevent saving when in view-only mode (mode=view AND edit toggle not activated)
    if eventid == 'recordexpenses_save_button' and create_mode == 'view' and not edit_mode:
        raise PreventUpdate

    # Set default outputs
    alert_open = False
    alert_color = ''
    alert_text = ''
    date_class = 'SingleDatePicker'
    payee_class= ''
    main_expense_id_class = ''
    sub_expense_id_class = ''
    particulars_class = ''
    amount_class = ''
    status_class = ''
    bur_no_class = ''
    submitted_by_class = ''
    confirmation_modal_open = False
    confirmation_message = ''
    btn_color = 'success'
    final_modal_open = False
    final_modal_header = ''
    
    if eventid == 'recordexpenses_save_button' and submitbtn:
        # Ensure required fields are filled
        def get_input_class(value):
            return 'red-border' if not value else 'form-control'
        if not all([exp_date, exp_payee, main_expense_id, sub_expense_id,
                exp_particulars, exp_amount, exp_bur_no, exp_submitted_by]) and not removerecord:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Missing required fields.'
            date_class = 'SingleDatePicker red-border' if not exp_date else 'SingleDatePicker'
            payee_class= get_input_class(exp_payee)
            main_expense_id_class = get_input_class(main_expense_id)
            sub_expense_id_class = get_input_class(sub_expense_id)
            particulars_class = get_input_class(exp_particulars)
            amount_class = get_input_class(exp_amount)
            status_class = get_input_class(exp_status)
            bur_no_class = get_input_class(exp_bur_no)
            submitted_by_class = get_input_class(exp_submitted_by)
        else: # all inputs are valid
            if create_mode == 'add':
                confirmation_modal_open = True
                confirmation_message = "Are you sure you want to add this expense record?"
            elif create_mode in ('edit', 'view'):
                confirmation_modal_open = True
                confirmation_message = "Are you sure you want to save changes to this expense record?"
                if removerecord:
                    confirmation_message = "Are you sure you want to delete this expense record?"
                    btn_color = 'danger'

    elif eventid == 'confirmation_modal_confirm' and confirmbtn:
        if confirmationmodal:
            if create_mode == 'add':
                sql = """ 
                    INSERT INTO adminteam.expenses (
                        exp_date, exp_payee, main_expense_id, sub_expense_id,
                        exp_particulars, exp_amount, exp_status, 
                        exp_bur_no, exp_submitted_by, exp_funding_source,
                        exp_receipt_link 
                    ) 
                            
                    VALUES (%s, %s, %s, %s, %s, %s, 2, %s, %s, %s, %s)
                """
                values = (
                    exp_date, exp_payee, main_expense_id, sub_expense_id, 
                    exp_particulars, exp_amount, exp_bur_no, 
                    exp_submitted_by, 
                    exp_funding_source if exp_funding_source else None,
                    exp_receipt_link if exp_receipt_link else None,
                )    
                try:
                    db.modifydatabase(sql, values)
                    final_modal_open = True
                    final_modal_header = "Expense Record Successfully Added."
                        
                except Exception as e:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = f'Error copying record: {e}'
                    return [alert_open, alert_color, alert_text]
        
            elif create_mode in ('edit', 'view'): 
                expid = parse_qs(parsed.query).get('id', [None])[0]
                
                if expid is None:
                    raise PreventUpdate

                sqlcode = """
                    UPDATE adminteam.expenses
                    SET
                        exp_date = %s,
                        exp_payee = %s, 
                        exp_particulars = %s, 
                        exp_status = %s,
                        exp_bur_no = %s,
                        exp_submitted_by = %s, 
                        exp_funding_source = %s,
                        exp_timestamp = CURRENT_TIMESTAMP,
                        exp_del_ind = %s,
                        exp_receipt_link = %s
                    WHERE 
                        exp_id = %s
                """
                to_delete = bool(removerecord)
                values = [
                    exp_date, exp_payee, exp_particulars,
                    exp_status, exp_bur_no, exp_submitted_by,
                    exp_funding_source if exp_funding_source else None,
                    to_delete,
                    exp_receipt_link if exp_receipt_link else None,
                    expid
                ]
                db.modifydatabase(sqlcode, values)

                final_modal_open = True
                final_modal_header = "Expense Record Edited Successfully."

            else:
                raise PreventUpdate

    elif eventid == 'confirmation_modal_cancel' and cancelbtn:
        if confirmationmodal:
            confirmation_modal_open = False
            confirmation_message = ''

    else:
        raise PreventUpdate   

    return [alert_open, alert_color, alert_text, date_class, payee_class, main_expense_id_class, sub_expense_id_class, particulars_class, amount_class,
            status_class, bur_no_class, submitted_by_class, confirmation_modal_open, confirmation_message, btn_color, final_modal_open, final_modal_header]
    

@app.callback(
    [
        Output('exp_date', 'date'),
        Output('exp_payee', 'value'),
        Output('main_expense_id', 'value'),
        Output('sub_expense_id', 'value'),
        Output('exp_particulars', 'value'),
        Output('exp_amount', 'value'),
        Output('exp_status', 'value'),
        Output('exp_bur_no', 'value'),
        Output('exp_submitted_by', 'value'),
        Output('exp_funding_source', 'value'),
        Output('exp_receipt', 'value') 
    ],
    [
        Input('recordexpenses_toload', 'modified_timestamp')
    ],
    [
        State('recordexpenses_toload', 'data'),
        State('url', 'search')
    ]
)
def recordexpenses_load(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        expidd = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT 
                exp_date, exp_payee, main_expense_id, sub_expense_id,
                exp_particulars, exp_amount, exp_status, 
                exp_bur_no, exp_submitted_by, exp_funding_source,
                exp_receipt_link as exp_receipt
            FROM adminteam.expenses
            WHERE exp_id = %s
        """
        values = [expidd]

        cols = [
            'exp_date', 'exp_payee',  'main_expense_id', 'sub_expense_id',
            'exp_particulars', 'exp_amount', 'exp_status', 
            'exp_bur_no', 'exp_submitted_by', 'exp_funding_source',
            'exp_receipt'
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        exp_date = df['exp_date'][0]
        exp_payee = df['exp_payee'][0]
        main_expense_id = df['main_expense_id'][0]
        sub_expense_id = df['sub_expense_id'][0]
        exp_particulars = df['exp_particulars'][0]
        exp_amount = df['exp_amount'][0]
        exp_status = df['exp_status'][0]
        exp_bur_no = df['exp_bur_no'][0]
        exp_submitted_by = df['exp_submitted_by'][0]
        exp_funding_source = df['exp_funding_source'][0]
        exp_receipt = df['exp_receipt'][0]
         
        return [
            exp_date, exp_payee,
            main_expense_id, sub_expense_id, exp_particulars,
            exp_amount, exp_status,
            exp_bur_no, exp_submitted_by, exp_funding_source, exp_receipt
        ]

    else:
        raise PreventUpdate
    

@app.callback(
    [ 
        Output('exp_date', 'disabled'),
        Output('exp_payee', 'disabled'),
        Output('main_expense_id', 'disabled'),
        Output('sub_expense_id', 'disabled'),
        Output('exp_particulars', 'disabled'),
        Output('exp_amount', 'disabled'),
        Output('exp_funding_source', 'disabled'),
        Output('exp_bur_no', 'disabled'),
        Output('exp_submitted_by', 'disabled'),
        Output('exp_receipt', 'disabled'), 
        Output('exp_date', 'style'),
        Output('exp_payee', 'style'),
        Output('main_expense_id', 'style'),
        Output('sub_expense_id', 'style'),
        Output('exp_particulars', 'style'),
        Output('exp_amount', 'style'),
        Output('exp_funding_source', 'style'),
        Output('exp_bur_no', 'style'),
        Output('exp_submitted_by', 'style'),
    ],
    [
        Input('url', 'search'),
        Input('addexpense_edit_mode', 'data'),
    ]
)
def addexpense_inputs_disabled(search, edit_mode):

    editable_disabled_style = {}
    # Initialize the "disabled" properties (booleans)
    date_display = payee_display = main_exense_display = sub_exense_display = (
        particulars_display 
    ) = amount_display = funding_source_display = bur_no_display = submitted_by_display = receipt_display = False

    # Initialize style properties as empty dictionaries instead of empty strings
    date_style = payee_style = main_expense_style = sub_exense_style = (
        particulars_style
    ) = amount_style = funding_source_style = bur_no_style = submitted_by_style = {}

    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        
        if create_mode == 'add':
            # In add mode we leave the disabled properties as False and styles as empty dicts
            pass
        elif create_mode == 'edit':
            main_exense_display = sub_exense_display = amount_display = True
        elif create_mode == 'view' and not edit_mode:
            # View-only mode: ALL fields disabled
            date_display = payee_display = main_exense_display = sub_exense_display = (
                particulars_display
            ) = amount_display = funding_source_display = bur_no_display = submitted_by_display = receipt_display = True
            date_style = payee_style = main_expense_style = sub_exense_style = (
                particulars_style
            ) = amount_style = funding_source_style = bur_no_style = submitted_by_style = editable_disabled_style
        elif create_mode == 'view' and edit_mode:
            # View mode toggled to edit: same as edit mode
            main_exense_display = sub_exense_display = amount_display = True

    return [
        date_display, payee_display, main_exense_display, sub_exense_display,
        particulars_display, amount_display, funding_source_display, bur_no_display,
        submitted_by_display, receipt_display,
        date_style, payee_style, main_expense_style, sub_exense_style,
        particulars_style, amount_style, funding_source_style, bur_no_style, submitted_by_style
    ]


# Callback to toggle edit mode when Edit button is clicked
@app.callback(
    Output('addexpense_edit_mode', 'data'),
    Input('addexpense_toggle_edit', 'n_clicks'),
    prevent_initial_call=True,
)
def addexpense_toggle_edit_mode(n_clicks):
    if n_clicks:
        return 1
    raise PreventUpdate


# Callback to show/hide Save/Cancel, Delete, Edit button, and Back button based on mode
@app.callback(
    [
        Output('recordexpenses_buttons_div', 'style'),
        Output('recordexpenses_removerecord_div', 'style'),
        Output('addexpense_toggle_edit', 'style'),
        Output('expenses_back_btn_div', 'style'),
    ],
    [
        Input('url', 'search'),
        Input('addexpense_edit_mode', 'data'),
    ]
)
def addexpense_update_action_visibility(search, edit_mode):
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]
    
    if create_mode == 'add':
        # Add mode: show save/cancel, hide delete, hide edit toggle, hide back
        return [{'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]
    elif create_mode == 'edit':
        # Edit mode: show save/cancel, show delete, hide edit toggle, hide back
        return [{'display': 'block'}, None, {'display': 'none'}, {'display': 'none'}]
    elif create_mode == 'view' and not edit_mode:
        # View-only: hide save/cancel, hide delete, show edit toggle, show back
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {"display": "flex", "justifyContent": "flex-end"}]
    elif create_mode == 'view' and edit_mode:
        # View toggled to edit: show save/cancel, show delete, hide edit toggle, hide back
        return [{'display': 'block'}, None, {'display': 'none'}, {'display': 'none'}]
    else:
        return [{'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]
