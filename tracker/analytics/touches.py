from typing import Optional

from .engine import Viz
from .types import Match

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class touchesXY(Viz):
    def __init__(self, x_range: Optional[tuple[float,float]], y_range: Optional[tuple[float,float]]):
        self.x_range = x_range
        self.y_range = y_range

    def name(self) -> str: 
        x = "" if self.x_range is None else f"X [{self.x_range}]"
        y = "" if self.y_range is None else f" and Y [{self.y_range}]"
        return "touches in " + x + y

    @property
    def description(self) -> str:
        return 'density heatmap of both teams players'
    
    def generate(self, match: Match) -> go.Figure:
        
        player_in_possesion = [] 
        player_teams = match.header.player_teams

        for frame in match.match:
            ball = frame.ball
            if ball is not None and ball.player is not None:
                p_id = ball.player

                # get player that has ball
                player = list(filter(lambda x: x.id == p_id, frame.players))
                if len(player) == 0:
                    continue
                player = player[0]
                
                # if x range exists and not in range then continue
                if self.x_range is not None \
                    and not (self.x_range[0] <= player.x <= self.x_range[1]):
                        continue

                # if y range exists and not in range then continue
                if self.y_range is not None \
                    and not (self.y_range[0] <= player.y <= self.y_range[1]):
                        continue

                if p_id in player_teams:
                    team = match.header.team1.name if player_teams[p_id] == "0" else match.header.team2.name
                    player_in_possesion.append({'x': player.x, 'y': player.y, 'team': team})

        df = pd.DataFrame(player_in_possesion)

        # Create density heatmaps for each team
        fig = px.density_heatmap(
            df, x='x', y='y', 
            facet_col='team', nbinsx=30, nbinsy=30, 
            title=self.name(), 
            marginal_x='violin', 
            range_x=[-53, 53], range_y=[-34, 34]
        )

        fig.update_traces(opacity=0.7)


        bg_img = dict(
            source=Viz.background(),
            xref="x",
            yref="y",
            x=-53,  # Adjust these values based on your field's dimensions and scale
            y=34,  # Adjust these values based on your field's dimensions and scale
            sizex=106,  # The width of your field in the same units as your x-axis
            sizey=68,  # The height of your field in the same units as your y-axis
            sizing="stretch",
            opacity=0.5,
            layer="below"
        )

        fig.add_layout_image(bg_img, row=1, col=1)
        fig.add_layout_image(bg_img, row=1, col=2)

        return fig

