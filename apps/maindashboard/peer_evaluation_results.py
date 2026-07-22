import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State, dash_table
from dash import callback_context
from dash import dcc
import io
from weasyprint import HTML
from flask import render_template
from apps.director import pdf_utils
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import base64
import os

from urllib.parse import urlparse, parse_qs
import flask


highlight_colors = { 
    'primary': "#0a4323",     # Main headers 
    'secondary': "#7a0911",   # Section titles 
    'accent': "#f8b237"       # Accent for borders/emphasis 
}

# A helper style for table borders
border_style = {
    "border": "1px solid #000",
    "padding": "5px"
}

editable_disabled_style = {
        "background-color": 'rgba(0,0,0,0)',
        "color": "black",
        "opacity": "1",
    }

summary = dbc.Container(
    [
        # Basic Information Section (Name, Peer Reviewers, etc.)
        dbc.Row(
            dbc.Col(
                html.Table(
                    children=[
                        html.Colgroup([
                            html.Col(style={"width": "20%"}),   # First column: smallest width
                            html.Col(style={"width": "35%"}), # Second column
                            html.Col(style={"width": "45%"})  # Third column, same as second
                        ]),
                        html.Tbody([
                            # Row 1
                            html.Tr([
                                html.Td("Name", style=border_style),
                                html.Td(
                                    dbc.Input(id="pr_name_input", type="text", placeholder="Enter name", disabled=True, style=editable_disabled_style),
                                    style=border_style
                                ),
                                html.Td("Peer Reviewers", style={**border_style, "text-align": "center"}),
                            ]),
                            # Row 2
                            html.Tr([
                                html.Td("For the period", style=border_style),
                                html.Td(
                                    dbc.Input(id="pr_period_input", type="text", placeholder="e.g. Jan 2025 - Mar 2025", disabled=True, style=editable_disabled_style),
                                    style=border_style
                                ),
                                html.Td(
                                    dbc.Textarea(id="pr_reviewers", placeholder="List of Reviewers", disabled=True, style=editable_disabled_style),
                                    rowSpan=2,
                                    style=border_style
                                ),
                            ]),
                            # Row 3
                            html.Tr([
                                html.Td("Dates Conducted", style=border_style),
                                html.Td(
                                    dbc.Input(id="pr_dates_conducted_input", type="text", placeholder="e.g. March 1, 2025", disabled=True, style=editable_disabled_style),
                                    style=border_style
                                ),
                            ]),
                        ])
                    ],
                    style={"width": "100%", "border-collapse": "collapse"}
                ),
                width=12
            ),
            id="basic_info_row",
            style={"margin-bottom": "20px"}
        ),

        # Evaluation Table
        dbc.Row(
            dbc.Col(
                html.Table(
                    children=[
                        # Table Header
                        html.Thead([
                            # First header row
                            html.Tr([
                                html.Th("Evaluation Parameters", rowSpan=2, style={**border_style, "verticalAlign": "middle"}),
                                html.Th("Peer Scores", colSpan=4, style={**border_style, "text-align": "center"}),
                                html.Th("Weighted Average", rowSpan=2, style={**border_style, "verticalAlign": "middle"}),
                            ]),
                            # Second header row (should align under "Peer Scores")
                            html.Tr([
                                html.Th("Beginning (1)", style={**border_style, "text-align": "center"}),
                                html.Th("Progressing (2)", style={**border_style, "text-align": "center"}),
                                html.Th("Competent (3)", style={**border_style, "text-align": "center"}),
                                html.Th("Advanced (4)", style={**border_style, "text-align": "center"}),
                            ])
                        ]),
                        # Table Body (Parameters)
                        html.Tbody([
                            html.Tr([
                                html.Td("Contributions", style=border_style),
                                html.Td(dbc.Input(id="pr_contributions_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_contributions_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_contributions_competent", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_contributions_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_contributions_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            html.Tr([
                                html.Td("Cooperation with Others", style=border_style),
                                html.Td(dbc.Input(id="pr_cooperation_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_cooperation_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_cooperation_competent", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_cooperation_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_cooperation_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            html.Tr([
                                html.Td("Focus and Commitments", style=border_style),
                                html.Td(dbc.Input(id="pr_focus_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_focus_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_focus_competent", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_focus_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_focus_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            html.Tr([
                                html.Td("Team Role Fulfillment", style=border_style),
                                html.Td(dbc.Input(id="pr_teamrole_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_teamrole_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_teamrole_competent", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_teamrole_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_teamrole_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            html.Tr([
                                html.Td("Ability to Communicate", style=border_style),
                                html.Td(dbc.Input(id="pr_communicate_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_communicate_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_communicate_competent", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_communicate_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_communicate_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            html.Tr([
                                html.Td("Completion of Assigned Task", style=border_style),
                                html.Td(dbc.Input(id="pr_completion_beginning", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_completion_progressing", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_completion_competent", type="number",disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_completion_advanced", type="number", disabled=True, style=editable_disabled_style), style=border_style),
                                html.Td(dbc.Input(id="pr_completion_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                            # Overall Weighted Average Row
                            html.Tr([
                                html.Td("Overall Weighted Average", colSpan=5, style={**border_style, "font-weight": "bold", "text-align": "right"}),
                                html.Td(dbc.Input(id="pr_overall_weighted_average", type="number", disabled=True, style=editable_disabled_style),
                                        style=border_style),
                            ]),
                        ]),
                    ],
                    style={"width": "100%", "border-collapse": "collapse"},
                    id="evaluation_table"
                ),
                width=12
            ),
            id="evaluation_table_row",
            style={"margin-bottom": "20px"}
        ),

        # Opportunities for Improvement
        dbc.Row(
            dbc.Col(
                [
                    html.Div("Opportunities for Improvement", 
                             style={"font-weight": "bold", "margin-bottom": "5px", "color": highlight_colors['secondary']}),
                    dbc.Textarea(
                        id="pr_opportunities_text",
                        placeholder="Enter opportunities for improvement here...",
                        disabled=True,
                        style={"width": "100%", "height": "100px"},
                    )
                ],
                width=12
            ),
            id="improvement_row",
            style={"margin-bottom": "20px"}
        ),

        # Sign-off Section (Conducted by, Date, Received by, Date)
        dbc.Row(
            dbc.Col(
                html.Table(
                    children=[
                        html.Tbody([
                            html.Tr([
                                html.Td([
                                    html.Div("Conducted by:", style={"margin-bottom": "5px"}),
                                    dbc.Select(id="pr_conducted_by", placeholder="Name", disabled=True, style=editable_disabled_style),
                                ], style=border_style),
                                html.Td([
                                    html.Div("Date:", style={"margin-bottom": "5px"}),
                                    dcc.DatePickerSingle(id="pr_conducted_date", className='SingleDatePicker', date=str(pd.to_datetime("today").date()),
                                                          placeholder="mm/dd/yyyy", disabled=True),
                                ], style=border_style),
                                html.Td([
                                    html.Div("Received by:", style={"margin-bottom": "5px"}),
                                    dbc.Select(id="pr_received_by", placeholder="Name", disabled=True, style=editable_disabled_style),
                                ], style=border_style),
                                html.Td([
                                    html.Div("Date:", style={"margin-bottom": "5px"}),
                                    dcc.DatePickerSingle(id="pr_received_date", className='SingleDatePicker', placeholder="mm/dd/yyyy", disabled=True),
                                ], style=border_style),
                            ])
                        ])
                    ],
                    style={"width": "100%", "border-collapse": "collapse"}
                ),
                width=12
            ),
            id="pr_sign_off_row",
            style={"margin-bottom": "20px"}
        ),

    ],
    fluid=True,
    style={"background-color": "#f4f4f4", "padding": "20px"}
)

remarks_section = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Table(
                    children=[
                        # Optional: You can tweak column widths as needed
                        html.Colgroup([
                            html.Col(style={"width": "20%"}),
                            html.Col(style={"width": "80%"}),
                        ]),
                        html.Tbody([
                            # Heading row for Anecdotes/Remarks/Opportunities
                            html.Tr([
                                html.Td(
                                    "Anecdotes / Remarks / Opportunities", 
                                    colSpan=2,
                                    style={
                                        **border_style, 
                                        "text-align": "center",
                                        "font-weight": "bold",
                                        "background-color": highlight_colors['accent']
                                    }
                                )
                            ]),
                            # Row for “Contribution”
                            html.Tr([
                                html.Td("Contribution", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="pr_remarks_contribution", 
                                        placeholder="No feedback received for Contribution...", 
                                        disabled=True,  # Set to False if you want it editable
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                            # Row for “Cooperation with Others”
                            html.Tr([
                                html.Td("Cooperation with Others", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="pr_remarks_cooperation", 
                                        placeholder="No feedback received for Cooperation with Others...", 
                                        disabled=True,
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                            # Row for “Focus and Commitments”
                            html.Tr([
                                html.Td("Focus and Commitments", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="pr_remarks_focus", 
                                        placeholder="No feedback received for Focus and Commitments...", 
                                        disabled=True,
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                            # Row for “Team Role Fulfillment”
                            html.Tr([
                                html.Td("Team Role Fulfillment", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="pr_remarks_team_role", 
                                        placeholder="No feedback received for Team Role Fulfillment...", 
                                        disabled=True,
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                            # Row for “Ability to Communicate”
                            html.Tr([
                                html.Td("Ability to Communicate", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="pr_remarks_communicate", 
                                        placeholder="No feedback received for Ability to Communicate...", 
                                        disabled=True,
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                            # Row for “Completion of Tasks”
                            html.Tr([
                                html.Td("Completion of Tasks", style=border_style),
                                html.Td(
                                    dbc.Textarea(
                                        id="pr_remarks_completion", 
                                        placeholder="No feedback received for Completion of Tasks...", 
                                        disabled=True,
                                        style=editable_disabled_style
                                    ),
                                    style=border_style
                                )
                            ]),
                        ])
                    ],
                    style={"width": "100%", "border-collapse": "collapse"}
                ),
                width=12
            ),
            style={"margin-bottom": "20px"}
        ),
    ],
    fluid=True,
    style={"background-color": "#f4f4f4", "padding": "20px"}
)


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.Div(  
                            [
                                dcc.Store(id='pr_response_to_load', storage_type='memory', data=0),
                                dcc.Download(id="pr_pdf-download")
                            ]
                        ),
                        html.Div(
                            # Top Header (Organization/Office Title)
                            dbc.Row(
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.H3("University of the Philippines", 
                                                    style={"margin-bottom": "0px", "text-align": "center", "color": highlight_colors['secondary'], "font-weight": "bold", "font-size": "2.5rem"}),
                                            html.H4("Quality Assurance Office Diliman", 
                                                    style={"margin-top": "0px", "text-align": "center", "color": highlight_colors['primary'], "font-size": "1.5rem"}),
                                            html.H5("PEER EVALUATION SUMMARY REPORT", 
                                                    style={
                                                        "text-align": "center", 
                                                        "margin-top": "30px",
                                                        "font-weight": "bold",
                                                        "font-size": "1.5rem",
                                                        "color": highlight_colors['accent']
                                                    }
                                            ),
                                        ],
                                        style={"margin-bottom": "5px"}  # reduce bottom margin of the header container
                                    ),
                                    width=12,
                                ),
                            ),
                            style={"margin-bottom": "0px"}  # reduce spacing after the header
                        ),
                        html.Hr(
                            style={
                                "margin-top": "0px",  # remove top margin from HR
                            }
                        ),
                        summary, 
                        html.Br(),
                        remarks_section,
                        html.Br(),
                        dbc.Alert(id='pr_response_summary_alert', is_open=False), # For feedback purpose
                        html.Div(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "Download PDF",
                                        id="pr_download_pdf_btn",
                                        n_clicks=0,
                                        color="secondary",
                                        style={"margin-left": "10px"}
                                    )
                                )
                            ],
                            id="pr_download_style_div"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Back",
                                                id="pr_back_button",
                                                color="primary",
                                                className="me-2",
                                                href="/homepage",
                                                style={
                                                    "display": "flex",          # make the button a flex container
                                                    "justifyContent": "center",# center horizontally
                                                    "alignItems": "center",    # center vertically
                                                    "fontWeight": "bold",      # bold text
                                                    "fontSize": "12px"         # at least 12px font size
                                                }
                                            ),
                                        ],
                                        style={
                                            "display": "flex",
                                            "justifyContent": "flex-end"   # keeps the button aligned to the right of its parent
                                        }
                                    ),
                                ),
                            ],
                            justify="end",
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Please Confirm Your Action"), className="bg-primary"),
                                dbc.ModalBody(
                                    html.H5("Are you sure you want to save the changes?"),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Cancel", id= "pr_summary_initial_modal_cancel", color="warning"),
                                        dbc.Button("Confirm", id= "pr_summary_initial_modal_confirm", color="success")
                                    ]
                                ),
                            ],
                            centered=True,
                            id="pr_summary_initial_modal",
                            backdrop=True,
                            className="modal-success",
                        ),

                        # Final Modal for Training Documents
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H3("Changes has been saved"), close_button=False, className="bg-success", style={"color": "white"}),
                                dbc.ModalBody(
                                    html.H5("Click Proceed to continue"),
                                ),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Proceed", href='/peer_evaluation_responses', color="success"),
                                    ]
                                ),
                            ],
                            centered=True,
                            id="pr_summary_last_modal",
                            backdrop="static",
                            className="modal-success",
                        ), 
                    ],
                    width=9,
                    style={"marginLeft": "15px"},
                )
            ]
        ),
        html.Br(),
        html.Br(),
        # Example Control Buttons (Optional)
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


@app.callback(
    [   
        Output('pr_received_by', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('currentuserid', 'data')
    ]
)

def load_received_by(pathname, currentuserid):
    if pathname == '/peer_evaluation_results':
        evaluatee_id = currentuserid

        sql = """
            SELECT
            CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) as label,
            u.user_id as value
            FROM maindashboard.users u
            WHERE u.user_id = %s
        """
        values = [evaluatee_id]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        received_by_options = df.to_dict('records')

    else:
        raise PreventUpdate
    return [received_by_options]


@app.callback(
    [   
        Output('pr_response_to_load', 'data'),
        Output('pr_back_button', 'style'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search'),
    ]
)
def peereval_get_userid(pathname, search):
    if pathname == '/peer_evaluation_results':
        create_mode = 'view'
        to_load = 1
        back_btn_div_style = {'display': 'flex', 'justifyContent': 'flex-end'}
    else:  
        raise PreventUpdate
    
    return [to_load, back_btn_div_style]

# evaluatee_id = parse_qs(parsed.query).get('id', [None])[0]

@app.callback(
    [
        Output('pr_name_input', 'value'),
        Output('pr_contributions_beginning', 'value'),
        Output('pr_contributions_progressing', 'value'),
        Output('pr_contributions_competent', 'value'),
        Output('pr_contributions_advanced', 'value'),
        Output('pr_contributions_weighted_average', 'value'),
        Output('pr_cooperation_beginning', 'value'),
        Output('pr_cooperation_progressing', 'value'),
        Output('pr_cooperation_competent', 'value'),
        Output('pr_cooperation_advanced', 'value'),
        Output('pr_cooperation_weighted_average', 'value'),
        Output('pr_focus_beginning', 'value'),
        Output('pr_focus_progressing', 'value'),
        Output('pr_focus_competent', 'value'),
        Output('pr_focus_advanced', 'value'),
        Output('pr_focus_weighted_average', 'value'),
        Output('pr_teamrole_beginning', 'value'),
        Output('pr_teamrole_progressing', 'value'),
        Output('pr_teamrole_competent', 'value'),
        Output('pr_teamrole_advanced', 'value'),
        Output('pr_teamrole_weighted_average', 'value'),
        Output('pr_communicate_beginning', 'value'),
        Output('pr_communicate_progressing', 'value'),
        Output('pr_communicate_competent', 'value'),
        Output('pr_communicate_advanced', 'value'),
        Output('pr_communicate_weighted_average', 'value'),
        Output('pr_completion_beginning', 'value'),
        Output('pr_completion_progressing', 'value'),
        Output('pr_completion_competent', 'value'),
        Output('pr_completion_advanced', 'value'),
        Output('pr_completion_weighted_average', 'value'),
        Output('pr_overall_weighted_average', 'value')
    ],
    [
        Input('pr_response_to_load', 'modified_timestamp')
    ],
    [
        State('pr_response_to_load', 'data'),
        State('currentuserid', 'data'),
    ]
)
def peereval_load(timestamp, to_load, currentuserid):
    if not to_load:
        raise PreventUpdate
    if to_load:
        evaluatee_id = currentuserid

    # Run one query for all rubric_ids (1 to 6)
    sql = """
        SELECT 
            CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) AS full_name,
            ed.rubric_id,
            ed.rating_value, 
            COUNT(*) AS rating_count
        FROM maindashboard.users u
        LEFT JOIN director.peer_evaluations pe ON u.user_id = pe.evaluatee_id
        LEFT JOIN director.evaluation_details ed ON pe.evaluation_id = ed.evaluation_id
        WHERE pe.evaluatee_id = %s
          AND pe.peer_eval_delete_ind = FALSE
          AND evaluation_period_id = (
            SELECT period_id   AS value
                FROM director.evaluation_periods
                WHERE active_status = TRUE
                AND period_del_ind = FALSE
            )
        GROUP BY full_name, ed.rubric_id, ed.rating_value;
    """
    values = [evaluatee_id]
    cols = ['full_name', 'rubric_id', 'rating_value', 'rating_count']
    df = db.querydatafromdatabase(sql, values, cols)
    
    # If no evaluation data, set default values.
    if df.empty:
        full_name = ""
        # For each rubric (1 to 6): 4 counts and a weighted average, all set to 0.
        result = {rubric: {1: 0, 2: 0, 3: 0, 4: 0, 'weighted': 0} for rubric in range(1, 7)}
    else:
        full_name = df['full_name'].iloc[0]
        # Initialize for all expected rubrics (1 to 6)
        result = {rubric: {1: 0, 2: 0, 3: 0, 4: 0, 'weighted': 0} for rubric in range(1, 7)}
        
        # Populate the result dictionary with counts from the query
        for _, row in df.iterrows():
            rubric = row['rubric_id']
            rating = row['rating_value']
            count = row['rating_count']
            result[rubric][rating] = count

        # Calculate weighted average for each rubric and round to 2 decimals.
        for rubric in range(1, 7):
            counts = result[rubric]
            total = counts[1] + counts[2] + counts[3] + counts[4]
            if total > 0:
                weighted = (1 * counts[1] + 2 * counts[2] + 3 * counts[3] + 4 * counts[4]) / total
            else:
                weighted = 0
            result[rubric]['weighted'] = round(weighted, 2)

    # Map rubric ids to your UI components.
    # Rubric 1: Contributions
    contributions_beginning    = result[1][1]
    contributions_progressing  = result[1][2]
    contributions_competent    = result[1][3]
    contributions_advanced     = result[1][4]
    contributions_weighted     = result[1]['weighted']

    # Rubric 2: Cooperation with Others
    cooperation_beginning      = result[2][1]
    cooperation_progressing    = result[2][2]
    cooperation_competent      = result[2][3]
    cooperation_advanced       = result[2][4]
    cooperation_weighted       = result[2]['weighted']

    # Rubric 3: Focus and Commitments
    focus_beginning            = result[3][1]
    focus_progressing          = result[3][2]
    focus_competent            = result[3][3]
    focus_advanced             = result[3][4]
    focus_weighted             = result[3]['weighted']

    # Rubric 4: Team Role Fulfillment
    teamrole_beginning         = result[4][1]
    teamrole_progressing       = result[4][2]
    teamrole_competent         = result[4][3]
    teamrole_advanced          = result[4][4]
    teamrole_weighted          = result[4]['weighted']

    # Rubric 5: Ability to Communicate
    communicate_beginning      = result[5][1]
    communicate_progressing    = result[5][2]
    communicate_competent      = result[5][3]
    communicate_advanced       = result[5][4]
    communicate_weighted       = result[5]['weighted']

    # Rubric 6: Completion of Assigned Task
    completion_beginning       = result[6][1]
    completion_progressing     = result[6][2]
    completion_competent       = result[6][3]
    completion_advanced        = result[6][4]
    completion_weighted        = result[6]['weighted']

    # Calculate overall weighted average as the average of the six rubric weighted averages.
    overall_weighted = round(
        (contributions_weighted + cooperation_weighted + focus_weighted +
         teamrole_weighted + communicate_weighted + completion_weighted) / 6, 2
    )

    return [
        full_name,
        contributions_beginning,
        contributions_progressing,
        contributions_competent,
        contributions_advanced,
        contributions_weighted,
        cooperation_beginning,
        cooperation_progressing,
        cooperation_competent,
        cooperation_advanced,
        cooperation_weighted,
        focus_beginning,
        focus_progressing,
        focus_competent,
        focus_advanced,
        focus_weighted,
        teamrole_beginning,
        teamrole_progressing,
        teamrole_competent,
        teamrole_advanced,
        teamrole_weighted,
        communicate_beginning,
        communicate_progressing,
        communicate_competent,
        communicate_advanced,
        communicate_weighted,
        completion_beginning,
        completion_progressing,
        completion_competent,
        completion_advanced,
        completion_weighted,
        overall_weighted
    ]


@app.callback(
    [
        Output('pr_period_input', 'value'),
        Output('pr_dates_conducted_input', 'value'),
        Output('pr_reviewers', 'value')
    ],
    [
        Input('pr_response_to_load', 'modified_timestamp')
    ],
    [
        State('pr_response_to_load', 'data'),
        State('url', 'search'),
        State('currentuserid', 'data')
    ]
)
def update_reviewers(timestamp, to_load, search, currentuserid):

    default_style = {
        "background-color": "white",
        "color": "black",
        "opacity": "1",
    }

    if not to_load:
        raise PreventUpdate

    if to_load:
        evaluatee_id = currentuserid

        # SQL query to get the distinct full names of evaluators who have evaluated the chosen evaluatee.
        sql = """
            SELECT DISTINCT 
                to_char(lower(period_details), 'Mon DD, YYYY') ||
                ' to ' ||
                to_char(upper(period_details) - INTERVAL '1 day', 'Mon DD, YYYY')
                AS evaluation_period
            FROM director.peer_evaluations pe
            JOIN director.evaluation_periods ep on ep.period_id = pe.evaluation_period_id 
            WHERE pe.evaluatee_id = %s
            AND pe.peer_eval_delete_ind = FALSE
            AND evaluation_period_id = (
                SELECT period_id   AS value
                    FROM director.evaluation_periods
                    WHERE active_status = TRUE
                    AND period_del_ind = FALSE
            );
        """
        values = [evaluatee_id]
        cols = ['evaluation_period']
        df = db.querydatafromdatabase(sql, values, cols)

        # If no evaluators are found, return an empty string.
        if df.empty:
            evaluation_period = ""
            dates_conducted = ""
            reviewers_text= "No peer review evaluations found."

        if not df.empty:
            evaluation_period = df['evaluation_period'][0]
            dates_conducted = df['evaluation_period'][0]
            # Combine the distinct evaluator names into a single string, separated by commas.
            reviewers_text = "Anonymous"

    
    return [evaluation_period, dates_conducted, reviewers_text]

@app.callback(
    [
        Output('pr_remarks_contribution',   'value'),
        Output('pr_remarks_cooperation',    'value'),
        Output('pr_remarks_focus',          'value'),
        Output('pr_remarks_team_role',      'value'),
        Output('pr_remarks_communicate',    'value'),
        Output('pr_remarks_completion',     'value'),
    ],
    [
        Input('pr_response_to_load', 'modified_timestamp')
    ],
    [
        State('pr_response_to_load', 'data'),
        State('url', 'search'),
        State('currentuserid', 'data')
    ]
)
def update_remarks(timestamp, to_load, search, currentuserid):
    # only run after the store is set
    if not to_load:
        raise PreventUpdate
    if to_load:
        # extract evaluatee_id from URL
        evaluatee_id = currentuserid
        if evaluatee_id is None:
            raise PreventUpdate

        # grab all feedback + evaluator names for this evaluatee
        sql = """
            SELECT
                ed.rubric_id,
                ed.feedback
            FROM director.peer_evaluations pe
            JOIN director.evaluation_details ed
            ON pe.evaluation_id = ed.evaluation_id
            JOIN maindashboard.users u
            ON pe.evaluator_id = u.user_id
            WHERE pe.evaluatee_id = %s
            AND evaluation_period_id = (
                SELECT period_id   AS value
                    FROM director.evaluation_periods
                    WHERE active_status = TRUE
                    AND period_del_ind = FALSE
            )
            AND pe.peer_eval_delete_ind = FALSE
            AND ed.feedback IS NOT NULL
            ORDER BY ed.rubric_id, pe.evaluation_date;
        """
        df = db.querydatafromdatabase(sql, [evaluatee_id], ['rubric_id', 'feedback'])

        # initialize empty lists for each rubric
        remarks_by_rubric = {i: [] for i in range(1,7)}

        # accumulate formatted entries
        for _, row in df.iterrows():
            r = row['rubric_id']
            text = row['feedback'].strip()
            remarks_by_rubric[r].append(f"{text}")

        # join entries with single line breaks, default to empty string
        return [
            "\n\n".join(remarks_by_rubric[1]),
            "\n\n".join(remarks_by_rubric[2]),
            "\n\n".join(remarks_by_rubric[3]),
            "\n\n".join(remarks_by_rubric[4]),
            "\n\n".join(remarks_by_rubric[5]),
            "\n\n".join(remarks_by_rubric[6]),
        ]

@app.callback(
    [
        Output('pr_opportunities_text', 'value'),
        Output('pr_conducted_by', 'value'),
        Output('pr_conducted_date', 'date'),
        Output('pr_received_by', 'value'),
        Output('pr_received_date', 'date'),
    ],
    [
        Input('pr_response_to_load', 'modified_timestamp')
    ],
    [
        State('pr_response_to_load', 'data'),
        State('url', 'search'),
        State('currentuserid', 'data')
    ]
)

def load_summary(timestamp, to_load, search, currentuserid):
    if to_load:
        evaluatee_id = currentuserid

        sql = """
            SELECT summary_text, summary_conducted_by, summary_conducted_date, summary_received_by, summary_received_date
            FROM director.evaluation_summaries
            WHERE summary_evaluatee_id = %s
            AND summary_evaluation_period = (
                SELECT period_id
                FROM director.evaluation_periods
                WHERE active_status = TRUE
                AND period_del_ind  = FALSE
            )
        """
        values = [evaluatee_id]
        cols = ['summary_text', 'summary_conducted_by', 'summary_conducted_date', 'summary_received_by', 'summary_received_date']
        df = db.querydatafromdatabase(sql, values, cols)

        if df.empty:
            summary_text = ""
            conducted_by = ""
            conducted_date = dash.no_update
            received_by = ""
            received_date = None  
        else:
            summary_text =df['summary_text'][0]
            conducted_by = df['summary_conducted_by'][0]
            conducted_date = df['summary_conducted_date'][0]
            received_by = df['summary_received_by'][0]
            received_date = df['summary_received_date'][0]

    else:
        raise PreventUpdate
    
    return [summary_text, conducted_by, conducted_date, received_by, received_date]


@app.callback(
    Output("pr_download_style_div", "style"),
    Input('url', 'pathname'),
    State('currentuserid', 'data')
)
def evaluation_summary_downloadbutton(pathname, currentuserid):

    download_button_style = {'display': 'none'}

    if pathname == '/peer_evaluation_results':
        id_evaluatee = currentuserid
        id_final = int(id_evaluatee)

        if not id_evaluatee:
            raise PreventUpdate
        
        sql = """
            SELECT COUNT(*) as count
        FROM director.evaluation_summaries
        WHERE summary_evaluatee_id = %s
        AND summary_evaluation_period = (
            SELECT period_id
            FROM director.evaluation_periods
            WHERE active_status = TRUE
            AND period_del_ind = FALSE
        )
        """
        values = [id_final]
        cols = ['count']
        df = db.querydatafromdatabase(sql, values, cols)
        sql_checker = int(df['count'][0])

        if sql_checker < 1:
            return {'display': 'none'}
        elif sql_checker > 0:
            return {'display': 'flex'}
        else:
            return download_button_style


@app.callback(
    Output("pr_pdf-download", "data"),
    Input("pr_download_pdf_btn", "n_clicks"),
    [State("url", "search"),
     State('currentuserid', 'data')],
    prevent_initial_call=True,
)

def serve_pdf(n_clicks, search, currentuserid):
    eval_id = currentuserid
    final_id = int(eval_id)

    if not eval_id:
        raise PreventUpdate
    sql = """
        SELECT
        CONCAT(u.user_fname, ' ', LEFT(u.user_mname, 1), '. ', u.user_sname, ' ', u.user_suffixname) as "Full_Name"
        FROM maindashboard.users u
        WHERE u.user_id = %s
    """
    values = [final_id]
    cols = ['Full_Name']
    df = db.querydatafromdatabase(sql, values, cols)
    full_name =df['Full_Name'][0]

    pdf = pdf_utils.generate_pdf_bytes(final_id)
    return dcc.send_bytes(lambda buf: buf.write(pdf), filename=f"Peer_Evaluation_Report_{full_name}.pdf")

