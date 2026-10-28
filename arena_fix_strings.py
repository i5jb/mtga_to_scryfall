#import re

def fix_mana_cost(s):
  manacosts = {
    'o(2/B)o(2/G)o(2/U)': '{2/B}{2/G}{2/U}',
    'o(2/B)o(2/R)o(2/G)': '{2/B}{2/R}{2/G}',
    'o(2/G)o(2/G)': '{2/G}{2/G}',
    'o(2/G)o(2/U)o(2/R)': '{2/G}{2/U}{2/R}',
    'o(2/R)o(2/R)o(2/R)': '{2/R}{2/R}{2/R}',
    'o(2/R)o(2/W)o(2/B)': '{2/R}{2/W}{2/B}',
    'o(2/U)o(2/R)o(2/W)': '{2/U}{2/R}{2/W}',
    'o(2/W)o(2/B)o(2/G)': '{2/W}{2/B}{2/G}',
    'o(2/W)o(2/U)o(2/B)o(2/R)o(2/G)': '{2/W}{2/U}{2/B}{2/R}{2/G}',
    'o(B/G)': '{B/G}',
    'o(B/G)o(B/G)': '{B/G}{B/G}',
    'o(B/G)o(B/G)o(B/G)': '{B/G}{B/G}{B/G}',
    'o(B/G)o(B/G)o(B/G)o(B/G)': '{B/G}{B/G}{B/G}{B/G}',
    'o(B/G)o(B/G)o4oBoG': '{B/G}{B/G}{4}{B}{G}',
    'o(B/G)o2oBoG': '{B/G}{2}{B}{G}',
    'o(B/P)': '{B/P}',
    'o(B/R)': '{B/R}',
    'o(B/R)o(B/R)': '{B/R}{B/R}',
    'o(B/R)o(B/R)o(B/R)': '{B/R}{B/R}{B/R}',
    'o(B/R)o(B/R)o(B/R)o(B/R)': '{B/R}{B/R}{B/R}{B/R}',
    'o(B/R)o(B/R)o4oBoR': '{B/R}{B/R}{4}{B}{R}',
    'o(B/R)o2oBoR': '{B/R}{2}{B}{R}',
    'o(C/W)o(C/U)o(C/B)o(C/R)o(C/G)': '{C/W}{C/U}{C/B}{C/R}{C/G}',
    'o(G/P)': '{G/P}',
    'o(G/U)': '{G/U}',
    'o(G/U)o(G/U)': '{G/U}{G/U}',
    'o(G/U)o(G/U)o(G/U)o(G/U)': '{G/U}{G/U}{G/U}{G/U}',
    'o(G/U)o(G/U)o1oGoU': '{G/U}{G/U}{1}{G}{U}',
    'o(G/U)o1oGoU': '{G/U}{1}{G}{U}',
    'o(G/W)': '{G/W}',
    'o(G/W)o(G/U)o(B/G)o(R/G)': '{G/W}{G/U}{B/G}{R/G}',
    'o(G/W)o(G/W)': '{G/W}{G/W}',
    'o(G/W)o(G/W)o(G/W)o(G/W)': '{G/W}{G/W}{G/W}{G/W}',
    'o(G/W)o(G/W)o4oGoW': '{G/W}{G/W}{4}{G}{W}',
    'o(G/W)o4oGoW': '{G/W}{4}{G}{W}',
    'o(G/W)oWo(W/U)': '{G/W}{W}{W/U}',
    'o(R/G)': '{R/G}',
    'o(R/G)o(R/G)': '{R/G}{R/G}',
    'o(R/G)o(R/G)o(R/G)o(R/G)': '{R/G}{R/G}{R/G}{R/G}',
    'o(R/G)o(R/G)o2oRoG': '{R/G}{R/G}{2}{R}{G}',
    'o(R/G)oGo(G/W)': '{R/G}{G}{G/W}',
    'o(R/W)': '{R/W}',
    'o(R/W)o(R/W)': '{R/W}{R/W}',
    'o(R/W)o(R/W)o(R/W)': '{R/W}{R/W}{R/W}',
    'o(R/W)o(R/W)o(R/W)o(R/W)': '{R/W}{R/W}{R/W}{R/W}',
    'o(R/W)o(R/W)o3oRoW': '{R/W}{R/W}{3}{R}{W}',
    'o(R/W)o2oRoW': '{R/W}{2}{R}{W}',
    'o(U/B)': '{U/B}',
    'o(U/B)': '{U/B}',
    'o(U/B)': '{U/B}',
    'o(U/B)o(U/B)': '{U/B}{U/B}',
    'o(U/B)o(U/B)o(U/B)': '{U/B}{U/B}{U/B}',
    'o(U/B)o(U/B)o(U/B)o(U/B)': '{U/B}{U/B}{U/B}{U/B}',
    'o(U/B)o(U/B)o(U/B)o(U/B)o(U/B)': '{U/B}{U/B}{U/B}{U/B}{U/B}',
    'o(U/P)': '{U/P}',
    'o(U/R)': '{U/R}',
    'o(U/R)o(U/R)': '{U/R}{U/R}',
    'o(U/R)o(U/R)o(U/R)o(U/R)': '{U/R}{U/R}{U/R}{U/R}',
    'o(U/R)o(U/R)oXoUoUoRoR': '{U/R}{U/R}{X}{U}{U}{R}{R}',
    'o(U/R)o4o(R/G)o(R/G)': '{U/R}{4}{R/G}{R/G}',
    'o(U/R)o4oUoR': '{U/R}{4}{U}{R}',
    'o(W/B)': '{W/B}',
    'o(W/B)o(W/B)': '{W/B}{W/B}',
    'o(W/B)o(W/B)o(W/B)o(W/B)': '{W/B}{W/B}{W/B}{W/B}',
    'o(W/B)o(W/B)o4oWoB': '{W/B}{W/B}{4}{W}{B}',
    'o(W/U)': '{W/U}',
    'o(W/U)o(U/B)o(B/R)o(R/G)o(G/W)': '{W/U}{U/B}{B/R}{R/G}{G/W}',
    'o(W/U)o(W/U)': '{W/U}{W/U}',
    'o(W/U)o(W/U)o(W/U)': '{W/U}{W/U}{W/U}',
    'o(W/U)o(W/U)o(W/U)o(W/U)': '{W/U}{W/U}{W/U}{W/U}',
    'o(W/U)o(W/U)o3oWoU': '{W/U}{W/U}{3}{W}{U}',
    'o(W/U)oUo(U/B)': '{W/U}{U}{U/B}',
    'o0': '{0}',
    'o1': '{1}',
    'o10': '{10}',
    'o10oBoB': '{10}{B}{B}',
    'o10oG': '{10}{G}',
    'o10oGoG': '{10}{G}{G}',
    'o10oRoR': '{10}{R}{R}',
    'o10oUoU': '{10}{U}{U}',
    'o11': '{11}',
    'o12': '{12}',
    'o13': '{13}',
    'o13oBoB': '{13}{B}{B}',
    'o14oG': '{14}{G}',
    'o15': '{15}',
    'o1o(B/G)': '{1}{B/G}',
    'o1o(B/G)o(B/G)': '{1}{B/G}{B/G}',
    'o1o(B/G)o4o(G/W)o(G/W)': '{1}{B/G}{4}{G/W}{G/W}',
    'o1o(B/P)': '{1}{B/P}',
    'o1o(B/P)o(B/P)': '{1}{B/P}{B/P}',
    'o1o(B/R)': '{1}{B/R}',
    'o1o(B/R)o(B/R)': '{1}{B/R}{B/R}',
    'o1o(B/R)oRo(R/G)': '{1}{B/R}{R}{R/G}',
    'o1o(G/U)': '{1}{G/U}',
    'o1o(G/U)o(G/U)': '{1}{G/U}{G/U}',
    'o1o(G/U)o4o(U/B)o(U/B)': '{1}{G/U}{4}{U/B}{U/B}',
    'o1o(G/W)': '{1}{G/W}',
    'o1o(G/W)o(G/W)': '{1}{G/W}{G/W}',
    'o1o(G/W)o(G/W)o(G/W)': '{1}{G/W}{G/W}{G/W}',
    'o1o(R/G)': '{1}{R/G}',
    'o1o(R/G)o(R/G)': '{1}{R/G}{R/G}',
    'o1o(R/G)o(R/G)o(R/G)': '{1}{R/G}{R/G}{R/G}',
    'o1o(R/G)oRoG': '{1}{R/G}{R}{G}',
    'o1o(R/W)': '{1}{R/W}',
    'o1o(R/W)o(R/W)': '{1}{R/W}{R/W}',
    'o1o(U/B)': '{1}{U/B}',
    'o1o(U/B)o(U/B)': '{1}{U/B}{U/B}',
    'o1o(U/B)o3oUoB': '{1}{U/B}{3}{U}{B}',
    'o1o(U/R)': '{1}{U/R}',
    'o1o(U/R)o(U/R)': '{1}{U/R}{U/R}',
    'o1o(W/B)': '{1}{W/B}',
    'o1o(W/B)o(W/B)': '{1}{W/B}{W/B}',
    'o1o(W/B)o(W/B)o(W/B)': '{1}{W/B}{W/B}{W/B}',
    'o1o(W/B)o2oWoB': '{1}{W/B}{2}{W}{B}',
    'o1o(W/B)o4o(B/R)o(B/R)': '{1}{W/B}{4}{B/R}{B/R}',
    'o1o(W/U)': '{1}{W/U}',
    'o1o(W/U)o(W/U)': '{1}{W/U}{W/U}',
    'o1o(W/U)o2oWoU': '{1}{W/U}{2}{W}{U}',
    'o1oB': '{1}{B}',
    'o1oBo(B/G)oG': '{1}{B}{B/G}{G}',
    'o1oBo3oG': '{1}{B}{3}{G}',
    'o1oBo3oW': '{1}{B}{3}{W}',
    'o1oBoB': '{1}{B}{B}',
    'o1oBoBo3oB': '{1}{B}{B}{3}{B}',
    'o1oBoBoB': '{1}{B}{B}{B}',
    'o1oBoBoBoB': '{1}{B}{B}{B}{B}',
    'o1oBoBoBoGoGoG': '{1}{B}{B}{B}{G}{G}{G}',
    'o1oBoBoG': '{1}{B}{B}{G}',
    'o1oBoBoRoR': '{1}{B}{B}{R}{R}',
    'o1oBoG': '{1}{B}{G}',
    'o1oBoGoG': '{1}{B}{G}{G}',
    'o1oBoGoU': '{1}{B}{G}{U}',
    'o1oBoR': '{1}{B}{R}',
    'o1oBoRoG': '{1}{B}{R}{G}',
    'o1oBoRoR': '{1}{B}{R}{R}',
    'o1oC': '{1}{C}',
    'o1oCoG': '{1}{C}{G}',
    'o1oCoR': '{1}{C}{R}',
    'o1oG': '{1}{G}',
    'o1oGo(G/U)oU': '{1}{G}{G/U}{U}',
    'o1oGo(G/W/P)oW': '{1}{G}{G/W/P}{W}',
    'o1oGo1oB': '{1}{G}{1}{B}',
    'o1oGoG': '{1}{G}{G}',
    'o1oGoGoG': '{1}{G}{G}{G}',
    'o1oGoGoGoG': '{1}{G}{G}{G}{G}',
    'o1oGoU': '{1}{G}{U}',
    'o1oGoUoR': '{1}{G}{U}{R}',
    'o1oGoUoU': '{1}{G}{U}{U}',
    'o1oGoW': '{1}{G}{W}',
    'o1oGoWoU': '{1}{G}{W}{U}',
    'o1oGoWoW': '{1}{G}{W}{W}',
    'o1oR': '{1}{R}',
    'o1oRo(R/W/P)oW': '{1}{R}{R/W/P}{W}',
    'o1oRo3oG': '{1}{R}{3}{G}',
    'o1oRo3oUoU': '{1}{R}{3}{U}{U}',
    'o1oRoG': '{1}{R}{G}',
    'o1oRoGoG': '{1}{R}{G}{G}',
    'o1oRoGoW': '{1}{R}{G}{W}',
    'o1oRoR': '{1}{R}{R}',
    'o1oRoRoG': '{1}{R}{R}{G}',
    'o1oRoRoR': '{1}{R}{R}{R}',
    'o1oRoRoRoR': '{1}{R}{R}{R}{R}',
    'o1oRoRoW': '{1}{R}{R}{W}',
    'o1oRoW': '{1}{R}{W}',
    'o1oRoWoB': '{1}{R}{W}{B}',
    'o1oRoWoW': '{1}{R}{W}{W}',
    'o1oRoXoBoB': '{1}{R}{X}{B}{B}',
    'o1oU': '{1}{U}',
    'o1oUo(U/R)oR': '{1}{U}{U/R}{R}',
    'o1oUo2oB': '{1}{U}{2}{B}',
    'o1oUo4oB': '{1}{U}{4}{B}',
    'o1oUoB': '{1}{U}{B}',
    'o1oUoBoB': '{1}{U}{B}{B}',
    'o1oUoBoR': '{1}{U}{B}{R}',
    'o1oUoR': '{1}{U}{R}',
    'o1oUoRoW': '{1}{U}{R}{W}',
    'o1oUoU': '{1}{U}{U}',
    'o1oUoUoRoR': '{1}{U}{U}{R}{R}',
    'o1oUoUoU': '{1}{U}{U}{U}',
    'o1oUoUoUoU': '{1}{U}{U}{U}{U}',
    'o1oUoW': '{1}{U}{W}',
    'o1oW': '{1}{W}',
    'o1oWo1oW': '{1}{W}{1}{W}',
    'o1oWo2oB': '{1}{W}{2}{B}',
    'o1oWo2oW': '{1}{W}{2}{W}',
    'o1oWo3oG': '{1}{W}{3}{G}',
    'o1oWo3oR': '{1}{W}{3}{R}',
    'o1oWo3oW': '{1}{W}{3}{W}',
    'o1oWo4oWoW': '{1}{W}{4}{W}{W}',
    'o1oWoB': '{1}{W}{B}',
    'o1oWoBoB': '{1}{W}{B}{B}',
    'o1oWoBoG': '{1}{W}{B}{G}',
    'o1oWoU': '{1}{W}{U}',
    'o1oWoUoB': '{1}{W}{U}{B}',
    'o1oWoUoBoR': '{1}{W}{U}{B}{R}',
    'o1oWoUoBoRoG': '{1}{W}{U}{B}{R}{G}',
    'o1oWoUoU': '{1}{W}{U}{U}',
    'o1oWoW': '{1}{W}{W}',
    'o1oWoWoB': '{1}{W}{W}{B}',
    'o1oWoWoBoB': '{1}{W}{W}{B}{B}',
    'o1oWoWoU': '{1}{W}{W}{U}',
    'o1oWoWoUoU': '{1}{W}{W}{U}{U}',
    'o1oWoWoW': '{1}{W}{W}{W}',
    'o1oWoWoWoW': '{1}{W}{W}{W}{W}',
    'o2': '{2}',
    'o2o(B/G)': '{2}{B/G}',
    'o2o(B/G)o(B/G)': '{2}{B/G}{B/G}',
    'o2o(B/R)': '{2}{B/R}',
    'o2o(B/R)o(B/R)': '{2}{B/R}{B/R}',
    'o2o(G/U)': '{2}{G/U}',
    'o2o(G/U)o(G/U)': '{2}{G/U}{G/U}',
    'o2o(G/U)o(G/U)o(G/U)': '{2}{G/U}{G/U}{G/U}',
    'o2o(G/W)': '{2}{G/W}',
    'o2o(G/W)o(G/W)': '{2}{G/W}{G/W}',
    'o2o(G/W)o(G/W)o(G/W)': '{2}{G/W}{G/W}{G/W}',
    'o2o(R/G)': '{2}{R/G}',
    'o2o(R/G)o(R/G)': '{2}{R/G}{R/G}',
    'o2o(R/W)': '{2}{R/W}',
    'o2o(R/W)o(R/W)': '{2}{R/W}{R/W}',
    'o2o(R/W)o(R/W)o(R/W)': '{2}{R/W}{R/W}{R/W}',
    'o2o(R/W)o4o(W/U)o(W/U)': '{2}{R/W}{4}{W/U}{W/U}',
    'o2o(U/B)': '{2}{U/B}',
    'o2o(U/B)o(U/B)': '{2}{U/B}{U/B}',
    'o2o(U/B)o(U/B)o(U/B)': '{2}{U/B}{U/B}{U/B}',
    'o2o(U/B)o(U/B)o3oUoB': '{2}{U/B}{U/B}{3}{U}{B}',
    'o2o(U/B)oBo(B/R)': '{2}{U/B}{B}{B/R}',
    'o2o(U/R)': '{2}{U/R}',
    'o2o(U/R)o(U/R)': '{2}{U/R}{U/R}',
    'o2o(W/B)': '{2}{W/B}',
    'o2o(W/B)o(W/B)': '{2}{W/B}{W/B}',
    'o2o(W/U)': '{2}{W/U}',
    'o2o(W/U)o(W/U)': '{2}{W/U}{W/U}',
    'o2oB': '{2}{B}',
    'o2oBo2oR': '{2}{B}{2}{R}',
    'o2oBo3oB': '{2}{B}{3}{B}',
    'o2oBo3oBoB': '{2}{B}{3}{B}{B}',
    'o2oBo6oBoB': '{2}{B}{6}{B}{B}',
    'o2oBoB': '{2}{B}{B}',
    'o2oBoBo5oUoU': '{2}{B}{B}{5}{U}{U}',
    'o2oBoBoB': '{2}{B}{B}{B}',
    'o2oBoBoG': '{2}{B}{B}{G}',
    'o2oBoBoGoG': '{2}{B}{B}{G}{G}',
    'o2oBoBoR': '{2}{B}{B}{R}',
    'o2oBoBoRoR': '{2}{B}{B}{R}{R}',
    'o2oBoG': '{2}{B}{G}',
    'o2oBoGoG': '{2}{B}{G}{G}',
    'o2oBoGoU': '{2}{B}{G}{U}',
    'o2oBoR': '{2}{B}{R}',
    'o2oBoRoG': '{2}{B}{R}{G}',
    'o2oC': '{2}{C}',
    'o2oG': '{2}{G}',
    'o2oGo(G/U/P)oU': '{2}{G}{G/U/P}{U}',
    'o2oGo2oU': '{2}{G}{2}{U}',
    'o2oGo3oG': '{2}{G}{3}{G}',
    'o2oGo3oGoG': '{2}{G}{3}{G}{G}',
    'o2oGo4oUoU': '{2}{G}{4}{U}{U}',
    'o2oGo5oG': '{2}{G}{5}{G}',
    'o2oGoG': '{2}{G}{G}',
    'o2oGoGoG': '{2}{G}{G}{G}',
    'o2oGoGoGoG': '{2}{G}{G}{G}{G}',
    'o2oGoGoU': '{2}{G}{G}{U}',
    'o2oGoGoUoU': '{2}{G}{G}{U}{U}',
    'o2oGoGoW': '{2}{G}{G}{W}',
    'o2oGoU': '{2}{G}{U}',
    'o2oGoUoR': '{2}{G}{U}{R}',
    'o2oGoUoU': '{2}{G}{U}{U}',
    'o2oGoW': '{2}{G}{W}',
    'o2oGoWoU': '{2}{G}{W}{U}',
    'o2oGoWoW': '{2}{G}{W}{W}',
    'o2oR': '{2}{R}',
    'o2oRo(G/W)': '{2}{R}{G/W}',
    'o2oRo(R/G/P)oG': '{2}{R}{R/G/P}{G}',
    'o2oRo1oG': '{2}{R}{1}{G}',
    'o2oRo1oR': '{2}{R}{1}{R}',
    'o2oRo2oR': '{2}{R}{2}{R}',
    'o2oRo2oW': '{2}{R}{2}{W}',
    'o2oRo3oRoR': '{2}{R}{3}{R}{R}',
    'o2oRo3oU': '{2}{R}{3}{U}',
    'o2oRo4oR': '{2}{R}{4}{R}',
    'o2oRo4oRoR': '{2}{R}{4}{R}{R}',
    'o2oRoG': '{2}{R}{G}',
    'o2oRoGoW': '{2}{R}{G}{W}',
    'o2oRoR': '{2}{R}{R}',
    'o2oRoRoG': '{2}{R}{R}{G}',
    'o2oRoRoGoG': '{2}{R}{R}{G}{G}',
    'o2oRoRoR': '{2}{R}{R}{R}',
    'o2oRoRoW': '{2}{R}{R}{W}',
    'o2oRoRoWoW': '{2}{R}{R}{W}{W}',
    'o2oRoW': '{2}{R}{W}',
    'o2oRoWoB': '{2}{R}{W}{B}',
    'o2oRoWoW': '{2}{R}{W}{W}',
    'o2oU': '{2}{U}',
    'o2oUo(U/P)': '{2}{U}{U/P}',
    'o2oUo1oR': '{2}{U}{1}{R}',
    'o2oUo2oR': '{2}{U}{2}{R}',
    'o2oUo3oUoU': '{2}{U}{3}{U}{U}',
    'o2oUo5oUoU': '{2}{U}{5}{U}{U}',
    'o2oUoB': '{2}{U}{B}',
    'o2oUoBoB': '{2}{U}{B}{B}',
    'o2oUoBoR': '{2}{U}{B}{R}',
    'o2oUoR': '{2}{U}{R}',
    'o2oUoRoW': '{2}{U}{R}{W}',
    'o2oUoU': '{2}{U}{U}',
    'o2oUoUoB': '{2}{U}{U}{B}',
    'o2oUoUoR': '{2}{U}{U}{R}',
    'o2oUoUoU': '{2}{U}{U}{U}',
    'o2oW': '{2}{W}',
    'o2oWo(W/B)oB': '{2}{W}{W/B}{B}',
    'o2oWo1oU': '{2}{W}{1}{U}',
    'o2oWo2oB': '{2}{W}{2}{B}',
    'o2oWo2oU': '{2}{W}{2}{U}',
    'o2oWoB': '{2}{W}{B}',
    'o2oWoBoB': '{2}{W}{B}{B}',
    'o2oWoBoG': '{2}{W}{B}{G}',
    'o2oWoU': '{2}{W}{U}',
    'o2oWoUoB': '{2}{W}{U}{B}',
    'o2oWoUoBoRoG': '{2}{W}{U}{B}{R}{G}',
    'o2oWoUoU': '{2}{W}{U}{U}',
    'o2oWoW': '{2}{W}{W}',
    'o2oWoWo3oWoW': '{2}{W}{W}{3}{W}{W}',
    'o2oWoWo5oUoU': '{2}{W}{W}{5}{U}{U}',
    'o2oWoWoB': '{2}{W}{W}{B}',
    'o2oWoWoBoB': '{2}{W}{W}{B}{B}',
    'o2oWoWoU': '{2}{W}{W}{U}',
    'o2oWoWoUoU': '{2}{W}{W}{U}{U}',
    'o2oWoWoW': '{2}{W}{W}{W}',
    'o2oWoWoWoW': '{2}{W}{W}{W}{W}',
    'o3': '{3}',
    'o3o(B/G)o(B/G)': '{3}{B/G}{B/G}',
    'o3o(B/R)': '{3}{B/R}',
    'o3o(B/R)o(B/R)': '{3}{B/R}{B/R}',
    'o3o(G/U)': '{3}{G/U}',
    'o3o(G/U)o(G/U)': '{3}{G/U}{G/U}',
    'o3o(G/W)o(G/W)': '{3}{G/W}{G/W}',
    'o3o(R/G)': '{3}{R/G}',
    'o3o(R/G)o(R/G)': '{3}{R/G}{R/G}',
    'o3o(R/W)': '{3}{R/W}',
    'o3o(R/W)o(R/W)': '{3}{R/W}{R/W}',
    'o3o(U/B)': '{3}{U/B}',
    'o3o(U/P)': '{3}{U/P}',
    'o3o(U/R)o(U/R)': '{3}{U/R}{U/R}',
    'o3o(W/B)': '{3}{W/B}',
    'o3o(W/B)o(W/B)': '{3}{W/B}{W/B}',
    'o3o(W/B)o(W/B)o(W/B)': '{3}{W/B}{W/B}{W/B}',
    'o3o(W/U)': '{3}{W/U}',
    'o3o(W/U)o(W/U)': '{3}{W/U}{W/U}',
    'o3oB': '{3}{B}',
    'o3oBo2oG': '{3}{B}{2}{G}',
    'o3oBoB': '{3}{B}{B}',
    'o3oBoBoB': '{3}{B}{B}{B}',
    'o3oBoBoG': '{3}{B}{B}{G}',
    'o3oBoBoRoR': '{3}{B}{B}{R}{R}',
    'o3oBoG': '{3}{B}{G}',
    'o3oBoGoU': '{3}{B}{G}{U}',
    'o3oBoR': '{3}{B}{R}',
    'o3oBoRoG': '{3}{B}{R}{G}',
    'o3oBoRoR': '{3}{B}{R}{R}',
    'o3oC': '{3}{C}',
    'o3oCoCoC': '{3}{C}{C}{C}',
    'o3oG': '{3}{G}',
    'o3oGoG': '{3}{G}{G}',
    'o3oGoGo(G/P)o(G/P)': '{3}{G}{G}{G/P}{G/P}',
    'o3oGoGoG': '{3}{G}{G}{G}',
    'o3oGoGoUoU': '{3}{G}{G}{U}{U}',
    'o3oGoGoW': '{3}{G}{G}{W}',
    'o3oGoGoWoW': '{3}{G}{G}{W}{W}',
    'o3oGoU': '{3}{G}{U}',
    'o3oGoUoR': '{3}{G}{U}{R}',
    'o3oGoUoU': '{3}{G}{U}{U}',
    'o3oGoW': '{3}{G}{W}',
    'o3oGoWoU': '{3}{G}{W}{U}',
    'o3oGoWoUoB': '{3}{G}{W}{U}{B}',
    'o3oGoWoW': '{3}{G}{W}{W}',
    'o3oR': '{3}{R}',
    'o3oRo(R/W)oW': '{3}{R}{R/W}{W}',
    'o3oRo2oU': '{3}{R}{2}{U}',
    'o3oRo4oRoR': '{3}{R}{4}{R}{R}',
    'o3oRoG': '{3}{R}{G}',
    'o3oRoGoG': '{3}{R}{G}{G}',
    'o3oRoGoW': '{3}{R}{G}{W}',
    'o3oRoR': '{3}{R}{R}',
    'o3oRoRoG': '{3}{R}{R}{G}',
    'o3oRoRoGoG': '{3}{R}{R}{G}{G}',
    'o3oRoRoR': '{3}{R}{R}{R}',
    'o3oRoRoW': '{3}{R}{R}{W}',
    'o3oRoW': '{3}{R}{W}',
    'o3oRoWoB': '{3}{R}{W}{B}',
    'o3oU': '{3}{U}',
    'o3oUo2oU': '{3}{U}{2}{U}',
    'o3oUo4oUoU': '{3}{U}{4}{U}{U}',
    'o3oUoB': '{3}{U}{B}',
    'o3oUoBoB': '{3}{U}{B}{B}',
    'o3oUoBoR': '{3}{U}{B}{R}',
    'o3oUoR': '{3}{U}{R}',
    'o3oUoRoR': '{3}{U}{R}{R}',
    'o3oUoRoW': '{3}{U}{R}{W}',
    'o3oUoU': '{3}{U}{U}',
    'o3oUoUoRoR': '{3}{U}{U}{R}{R}',
    'o3oUoUoU': '{3}{U}{U}{U}',
    'o3oW': '{3}{W}',
    'o3oWo2oW': '{3}{W}{2}{W}',
    'o3oWoB': '{3}{W}{B}',
    'o3oWoBoG': '{3}{W}{B}{G}',
    'o3oWoBoXoBoG': '{3}{W}{B}{X}{B}{G}',
    'o3oWoU': '{3}{W}{U}',
    'o3oWoUoB': '{3}{W}{U}{B}',
    'o3oWoUoBoR': '{3}{W}{U}{B}{R}',
    'o3oWoUoBoRoG': '{3}{W}{U}{B}{R}{G}',
    'o3oWoW': '{3}{W}{W}',
    'o3oWoWoBoB': '{3}{W}{W}{B}{B}',
    'o3oWoWoW': '{3}{W}{W}{W}',
    'o3oWoWoWoW': '{3}{W}{W}{W}{W}',
    'o4': '{4}',
    'o4o(B/G)': '{4}{B/G}',
    'o4o(B/P)o(B/P)o(B/P)': '{4}{B/P}{B/P}{B/P}',
    'o4o(B/R)o(B/R)': '{4}{B/R}{B/R}',
    'o4o(G/U)o(G/U)': '{4}{G/U}{G/U}',
    'o4o(G/W)': '{4}{G/W}',
    'o4o(G/W)o(G/W)': '{4}{G/W}{G/W}',
    'o4o(R/G)': '{4}{R/G}',
    'o4o(R/G)o(R/G)': '{4}{R/G}{R/G}',
    'o4o(R/W)o(R/W)': '{4}{R/W}{R/W}',
    'o4o(U/B)o(U/B)': '{4}{U/B}{U/B}',
    'o4o(W/B)o(W/B)': '{4}{W/B}{W/B}',
    'o4o(W/U)o(W/U)': '{4}{W/U}{W/U}',
    'o4oB': '{4}{B}',
    'o4oBo(B/P)': '{4}{B}{B/P}',
    'o4oBoB': '{4}{B}{B}',
    'o4oBoBoB': '{4}{B}{B}{B}',
    'o4oBoBoBoB': '{4}{B}{B}{B}{B}',
    'o4oBoG': '{4}{B}{G}',
    'o4oBoGoU': '{4}{B}{G}{U}',
    'o4oBoR': '{4}{B}{R}',
    'o4oBoRoG': '{4}{B}{R}{G}',
    'o4oBoRoR': '{4}{B}{R}{R}',
    'o4oG': '{4}{G}',
    'o4oGoG': '{4}{G}{G}',
    'o4oGoGoG': '{4}{G}{G}{G}',
    'o4oGoGoU': '{4}{G}{G}{U}',
    'o4oGoU': '{4}{G}{U}',
    'o4oGoUoR': '{4}{G}{U}{R}',
    'o4oGoW': '{4}{G}{W}',
    'o4oGoWoU': '{4}{G}{W}{U}',
    'o4oR': '{4}{R}',
    'o4oRoG': '{4}{R}{G}',
    'o4oRoR': '{4}{R}{R}',
    'o4oRoRoG': '{4}{R}{R}{G}',
    'o4oRoRoGoG': '{4}{R}{R}{G}{G}',
    'o4oRoRoR': '{4}{R}{R}{R}',
    'o4oRoRoW': '{4}{R}{R}{W}',
    'o4oRoW': '{4}{R}{W}',
    'o4oU': '{4}{U}',
    'o4oUoB': '{4}{U}{B}',
    'o4oUoBoR': '{4}{U}{B}{R}',
    'o4oUoR': '{4}{U}{R}',
    'o4oUoRoR': '{4}{U}{R}{R}',
    'o4oUoRoW': '{4}{U}{R}{W}',
    'o4oUoU': '{4}{U}{U}',
    'o4oUoUoU': '{4}{U}{U}{U}',
    'o4oW': '{4}{W}',
    'o4oWoB': '{4}{W}{B}',
    'o4oWoBoG': '{4}{W}{B}{G}',
    'o4oWoU': '{4}{W}{U}',
    'o4oWoUoB': '{4}{W}{U}{B}',
    'o4oWoW': '{4}{W}{W}',
    'o4oWoWoBoB': '{4}{W}{W}{B}{B}',
    'o4oWoWoW': '{4}{W}{W}{W}',
    'o5': '{5}',
    'o5o(B/R)o(B/R)': '{5}{B/R}{B/R}',
    'o5o(G/U)o(G/U)': '{5}{G/U}{G/U}',
    'o5o(R/G)o(R/G)': '{5}{R/G}{R/G}',
    'o5o(U/B)': '{5}{U/B}',
    'o5o(U/B)o(U/B)': '{5}{U/B}{U/B}',
    'o5oB': '{5}{B}',
    'o5oBoB': '{5}{B}{B}',
    'o5oBoBoB': '{5}{B}{B}{B}',
    'o5oBoG': '{5}{B}{G}',
    'o5oBoGoU': '{5}{B}{G}{U}',
    'o5oBoR': '{5}{B}{R}',
    'o5oC': '{5}{C}',
    'o5oCoC': '{5}{C}{C}',
    'o5oG': '{5}{G}',
    'o5oGoG': '{5}{G}{G}',
    'o5oGoGoG': '{5}{G}{G}{G}',
    'o5oGoU': '{5}{G}{U}',
    'o5oGoUoR': '{5}{G}{U}{R}',
    'o5oGoW': '{5}{G}{W}',
    'o5oR': '{5}{R}',
    'o5oRoG': '{5}{R}{G}',
    'o5oRoGoW': '{5}{R}{G}{W}',
    'o5oRoR': '{5}{R}{R}',
    'o5oRoRoR': '{5}{R}{R}{R}',
    'o5oRoW': '{5}{R}{W}',
    'o5oU': '{5}{U}',
    'o5oUoB': '{5}{U}{B}',
    'o5oUoBoR': '{5}{U}{B}{R}',
    'o5oUoR': '{5}{U}{R}',
    'o5oUoU': '{5}{U}{U}',
    'o5oUoUoU': '{5}{U}{U}{U}',
    'o5oW': '{5}{W}',
    'o5oWoB': '{5}{W}{B}',
    'o5oWoU': '{5}{W}{U}',
    'o5oWoW': '{5}{W}{W}',
    'o5oWoWoW': '{5}{W}{W}{W}',
    'o6': '{6}',
    'o6oB': '{6}{B}',
    'o6oBoB': '{6}{B}{B}',
    'o6oBoBoB': '{6}{B}{B}{B}',
    'o6oBoG': '{6}{B}{G}',
    'o6oBoR': '{6}{B}{R}',
    'o6oCoC': '{6}{C}{C}',
    'o6oG': '{6}{G}',
    'o6oGoG': '{6}{G}{G}',
    'o6oGoGoG': '{6}{G}{G}{G}',
    'o6oR': '{6}{R}',
    'o6oRoG': '{6}{R}{G}',
    'o6oRoGoW': '{6}{R}{G}{W}',
    'o6oRoR': '{6}{R}{R}',
    'o6oRoRoR': '{6}{R}{R}{R}',
    'o6oU': '{6}{U}',
    'o6oUoR': '{6}{U}{R}',
    'o6oUoU': '{6}{U}{U}',
    'o6oUoUoU': '{6}{U}{U}{U}',
    'o6oW': '{6}{W}',
    'o6oWoU': '{6}{W}{U}',
    'o6oWoUoB': '{6}{W}{U}{B}',
    'o6oWoW': '{6}{W}{W}',
    'o6oWoWoW': '{6}{W}{W}{W}',
    'o7': '{7}',
    'o7oB': '{7}{B}',
    'o7oBoB': '{7}{B}{B}',
    'o7oBoBoB': '{7}{B}{B}{B}',
    'o7oBoG': '{7}{B}{G}',
    'o7oG': '{7}{G}',
    'o7oGoG': '{7}{G}{G}',
    'o7oGoGoG': '{7}{G}{G}{G}',
    'o7oR': '{7}{R}',
    'o7oRoR': '{7}{R}{R}',
    'o7oRoRoR': '{7}{R}{R}{R}',
    'o7oU': '{7}{U}',
    'o7oUoU': '{7}{U}{U}',
    'o7oUoUoU': '{7}{U}{U}{U}',
    'o7oW': '{7}{W}',
    'o7oWoW': '{7}{W}{W}',
    'o8': '{8}',
    'o8oCoC': '{8}{C}{C}',
    'o8oG': '{8}{G}',
    'o8oGoGoG': '{8}{G}{G}{G}',
    'o8oR': '{8}{R}',
    'o8oRoR': '{8}{R}{R}',
    'o8oUoB': '{8}{U}{B}',
    'o8oUoU': '{8}{U}{U}',
    'o8oUoUoU': '{8}{U}{U}{U}',
    'o8oUoUoUoU': '{8}{U}{U}{U}{U}',
    'o8oW': '{8}{W}',
    'o9': '{9}',
    'o9oB': '{9}{B}',
    'oB': '{B}',
    'oBo(B/G)oG': '{B}{B/G}{G}',
    'oBo1oR': '{B}{1}{R}',
    'oBoB': '{B}{B}',
    'oBoBoB': '{B}{B}{B}',
    'oBoBoBoB': '{B}{B}{B}{B}',
    'oBoBoBoBoB': '{B}{B}{B}{B}{B}',
    'oBoBoBoBoBoB': '{B}{B}{B}{B}{B}{B}',
    'oBoBoG': '{B}{B}{G}',
    'oBoBoGoG': '{B}{B}{G}{G}',
    'oBoBoGoGoGoUoU': '{B}{B}{G}{G}{G}{U}{U}',
    'oBoBoR': '{B}{B}{R}',
    'oBoBoRoR': '{B}{B}{R}{R}',
    'oBoG': '{B}{G}',
    'oBoGoU': '{B}{G}{U}',
    'oBoR': '{B}{R}',
    'oBoRoG': '{B}{R}{G}',
    'oBoRoR': '{B}{R}{R}',
    'oC': '{C}',
    'oG': '{G}',
    'oGo(G/U)oU': '{G}{G/U}{U}',
    'oGo(G/W)oW': '{G}{G/W}{W}',
    'oGo1oB': '{G}{1}{B}',
    'oGo1oW': '{G}{1}{W}',
    'oGoG': '{G}{G}',
    'oGoGoG': '{G}{G}{G}',
    'oGoGoGoG': '{G}{G}{G}{G}',
    'oGoGoGoGoG': '{G}{G}{G}{G}{G}',
    'oGoGoGoUoUoU': '{G}{G}{G}{U}{U}{U}',
    'oGoGoU': '{G}{G}{U}',
    'oGoGoUoU': '{G}{G}{U}{U}',
    'oGoGoUoUoUoRoR': '{G}{G}{U}{U}{U}{R}{R}',
    'oGoGoWoW': '{G}{G}{W}{W}',
    'oGoU': '{G}{U}',
    'oGoUoR': '{G}{U}{R}',
    'oGoUoU': '{G}{U}{U}',
    'oGoW': '{G}{W}',
    'oGoWoU': '{G}{W}{U}',
    'oGoWoUoB': '{G}{W}{U}{B}',
    'oGoWoW': '{G}{W}{W}',
    'oR': '{R}',
    'oRo(R/W)oW': '{R}{R/W}{W}',
    'oRo2oR': '{R}{2}{R}',
    'oRoG': '{R}{G}',
    'oRoGoW': '{R}{G}{W}',
    'oRoGoWoU': '{R}{G}{W}{U}',
    'oRoR': '{R}{R}',
    'oRoRoG': '{R}{R}{G}',
    'oRoRoGoG': '{R}{R}{G}{G}',
    'oRoRoR': '{R}{R}{R}',
    'oRoRoRoR': '{R}{R}{R}{R}',
    'oRoRoWoW': '{R}{R}{W}{W}',
    'oRoRoWoWoWoBoB': '{R}{R}{W}{W}{W}{B}{B}',
    'oRoW': '{R}{W}',
    'oRoWoB': '{R}{W}{B}',
    'oRoWoU': '{R}{W}{U}',
    'oRoWoW': '{R}{W}{W}',
    'oU': '{U}',
    'oUo(U/R)oR': '{U}{U/R}{R}',
    'oUo3oU': '{U}{3}{U}',
    'oUo4oG': '{U}{4}{G}',
    'oUo4oU': '{U}{4}{U}',
    'oUoB': '{U}{B}',
    'oUoBoB': '{U}{B}{B}',
    'oUoBoBoBoR': '{U}{B}{B}{B}{R}',
    'oUoBoR': '{U}{B}{R}',
    'oUoR': '{U}{R}',
    'oUoRoR': '{U}{R}{R}',
    'oUoRoW': '{U}{R}{W}',
    'oUoU': '{U}{U}',
    'oUoUoBoB': '{U}{U}{B}{B}',
    'oUoUoBoBoBoRoR': '{U}{U}{B}{B}{B}{R}{R}',
    'oUoUoR': '{U}{U}{R}',
    'oUoUoRoR': '{U}{U}{R}{R}',
    'oUoUoRoRoRoWoW': '{U}{U}{R}{R}{R}{W}{W}',
    'oUoUoU': '{U}{U}{U}',
    'oUoUoUoRoRoR': '{U}{U}{U}{R}{R}{R}',
    'oUoUoUoU': '{U}{U}{U}{U}',
    'oW': '{W}',
    'oWo(W/B)oB': '{W}{W/B}{B}',
    'oWoB': '{W}{B}',
    'oWoBoB': '{W}{B}{B}',
    'oWoBoG': '{W}{B}{G}',
    'oWoU': '{W}{U}',
    'oWoUo(B/P)oRoG': '{W}{U}{B/P}{R}{G}',
    'oWoUoB': '{W}{U}{B}',
    'oWoUoBoR': '{W}{U}{B}{R}',
    'oWoUoBoRoG': '{W}{U}{B}{R}{G}',
    'oWoUoU': '{W}{U}{U}',
    'oWoW': '{W}{W}',
    'oWoWoB': '{W}{W}{B}',
    'oWoWoBoB': '{W}{W}{B}{B}',
    'oWoWoBoBoBoGoG': '{W}{W}{B}{B}{B}{G}{G}',
    'oWoWoUoU': '{W}{W}{U}{U}',
    'oWoWoUoUoBoBoRoRoGoG': '{W}{W}{U}{U}{B}{B}{R}{R}{G}{G}',
    'oWoWoW': '{W}{W}{W}',
    'oWoWoWoW': '{W}{W}{W}{W}',
    'oWoWoWoWoW': '{W}{W}{W}{W}{W}',
    'oX': '{X}',
    'oXo(G/U)o(G/U)': '{X}{G/U}{G/U}',
    'oXo1oW': '{X}{1}{W}',
    'oXo2oBoR': '{X}{2}{B}{R}',
    'oXo2oG': '{X}{2}{G}',
    'oXo2oGoG': '{X}{2}{G}{G}',
    'oXo2oGoU': '{X}{2}{G}{U}',
    'oXo2oR': '{X}{2}{R}',
    'oXo2oU': '{X}{2}{U}',
    'oXo2oW': '{X}{2}{W}',
    'oXo3oW': '{X}{3}{W}',
    'oXo4': '{X}{4}',
    'oXo6': '{X}{6}',
    'oXoB': '{X}{B}',
    'oXoBoB': '{X}{B}{B}',
    'oXoBoBoB': '{X}{B}{B}{B}',
    'oXoBoG': '{X}{B}{G}',
    'oXoBoGoU': '{X}{B}{G}{U}',
    'oXoBoR': '{X}{B}{R}',
    'oXoCoC': '{X}{C}{C}',
    'oXoG': '{X}{G}',
    'oXoGoG': '{X}{G}{G}',
    'oXoGoGoG': '{X}{G}{G}{G}',
    'oXoGoGoU': '{X}{G}{G}{U}',
    'oXoGoU': '{X}{G}{U}',
    'oXoGoW': '{X}{G}{W}',
    'oXoGoWoW': '{X}{G}{W}{W}',
    'oXoGoXoRoR': '{X}{G}{X}{R}{R}',
    'oXoR': '{X}{R}',
    'oXoRoG': '{X}{R}{G}',
    'oXoRoGoW': '{X}{R}{G}{W}',
    'oXoRoR': '{X}{R}{R}',
    'oXoRoRoGoG': '{X}{R}{R}{G}{G}',
    'oXoRoRoR': '{X}{R}{R}{R}',
    'oXoRoW': '{X}{R}{W}',
    'oXoU': '{X}{U}',
    'oXoUoR': '{X}{U}{R}',
    'oXoUoU': '{X}{U}{U}',
    'oXoUoUoRoR': '{X}{U}{U}{R}{R}',
    'oXoUoUoU': '{X}{U}{U}{U}',
    'oXoUoUoUoU': '{X}{U}{U}{U}{U}',
    'oXoW': '{X}{W}',
    'oXoWoB': '{X}{W}{B}',
    'oXoWoBoG': '{X}{W}{B}{G}',
    'oXoWoU': '{X}{W}{U}',
    'oXoWoUoU': '{X}{W}{U}{U}',
    'oXoWoW': '{X}{W}{W}',
    'oXoWoWoW': '{X}{W}{W}{W}',
    'oXoX': '{X}{X}',
    'oXoXo2oW': '{X}{X}{2}{W}',
    'oXoXo2oWoW': '{X}{X}{2}{W}{W}',
    'oXoXoB': '{X}{X}{B}',
    'oXoXoBoBoBoB': '{X}{X}{B}{B}{B}{B}',
    'oXoXoG': '{X}{X}{G}',
    'oXoXoGoG': '{X}{X}{G}{G}',
    'oXoXoR': '{X}{X}{R}',
    'oXoXoU': '{X}{X}{U}',
    'oXoXoUoU': '{X}{X}{U}{U}',
    'oXoXoUoUoUoU': '{X}{X}{U}{U}{U}{U}',
    'oXoXoW': '{X}{X}{W}',
    'oXoXoWoW': '{X}{X}{W}{W}',
    'oXoXoX': '{X}{X}{X}',
    'oXoXoXoGoU': '{X}{X}{X}{G}{U}',
    'oXoXoXoRoR': '{X}{X}{X}{R}{R}',
  }
  if s not in manacosts:
    print(f"Unknown manacost: '{s}'")
    return '{0}'
  return manacosts[s]

def strip_string(s):
  s = s.replace('<sprite="SpriteSheet_MiscIcons" name="arena_a">', 'A-')
  s = s.replace('<i>', '')
  s = s.replace('</i>', '')
  s = s.replace('<nobr>', '')
  s = s.replace('</nobr>', '')
  s = s.replace('•<indent=4%>', '• <indent=4%>')
  s = s.replace('<indent=4%>', '')
  s = s.replace('</indent>', '')

  s = s.replace('{o(2/U)o(2/B)o(2/R)o(2/G)}', '{2/U}{2/B}{2/R}{2/G}')
  s = s.replace('{o(B/G)o(B/G)o(B/G)o(B/G)}', '{B/G}{B/G}{B/G}{B/G}')
  s = s.replace('{o(B/G)o(B/G)o(B/G)}', '{B/G}{B/G}{B/G}')
  s = s.replace('{o(B/G)}', '{B/G}')
  s = s.replace('{o(B/P)o(B/P)}', '{B/P}{B/P}')
  s = s.replace('{o(B/R)o(B/R)o(B/R)o(B/R)}', '{B/R}{B/R}{B/R}{B/R}')
  s = s.replace('{o(B/R)o(B/R)o(B/R)}', '{B/R}{B/R}{B/R}')
  s = s.replace('{o(B/R)}', '{B/R}')
  s = s.replace('{o(G/P)o(G/P)}', '{G/P}{G/P}')
  s = s.replace('{o(G/U)o(G/U)o(G/U)o(G/U)}', '{G/U}{G/U}{G/U}{G/U}')
  s = s.replace('{o(G/U)o(G/U)}', '{G/U}{G/U}')
  s = s.replace('{o(G/U)}', '{G/U}')
  s = s.replace('{o(G/W)o(G/W)o(G/W)o(G/W)}', '{G/W}{G/W}{G/W}{G/W}')
  s = s.replace('{o(G/W)o(G/W)o(G/W)}', '{G/W}{G/W}{G/W}')
  s = s.replace('{o(G/W)o(G/W)}', '{G/W}{G/W}')
  s = s.replace('{o(G/W)}', '{G/W}')
  s = s.replace('{o(R/G)o(R/G)o(R/G)o(R/G)}', '{R/G}{R/G}{R/G}{R/G}')
  s = s.replace('{o(R/G)o(R/G)}', '{R/G}{R/G}')
  s = s.replace('{o(R/G)}', '{R/G}')
  s = s.replace('{o(R/W)o(R/W)o(R/W)o(R/W)o(R/W)o(R/W)}', '{R/W}{R/W}{R/W}{R/W}{R/W}{R/W}')
  s = s.replace('{o(R/W)o(R/W)o(R/W)o(R/W)}', '{R/W}{R/W}{R/W}{R/W}')
  s = s.replace('{o(R/W)o(R/W)o(R/W)}', '{R/W}{R/W}{R/W}')
  s = s.replace('{o(R/W)o(R/W)}', '{R/W}{R/W}')
  s = s.replace('{o(R/W)}', '{R/W}')
  s = s.replace('{o(U/B)o(U/B)o(U/B)o(U/B)}', '{U/B}{U/B}{U/B}{U/B}')
  s = s.replace('{o(U/B)o(U/B)}', '{U/B}{U/B}')
  s = s.replace('{o(U/B)}', '{U/B}')
  s = s.replace('{o(U/P)}', '{U/P}')
  s = s.replace('{o(U/R)o(U/R)o(U/R)o(U/R)}', '{U/R}{U/R}{U/R}{U/R}')
  s = s.replace('{o(U/R)o(U/R)}', '{U/R}{U/R}')
  s = s.replace('{o(U/R)}', '{U/R}')
  s = s.replace('{o(W/B)o(W/B)o(W/B)o(W/B)}', '{W/B}{W/B}{W/B}{W/B}')
  s = s.replace('{o(W/B)o(W/B)o(W/B)}', '{W/B}{W/B}{W/B}')
  s = s.replace('{o(W/B)o(W/B)}', '{W/B}{W/B}')
  s = s.replace('{o(W/B)}', '{W/B}')
  s = s.replace('{o(W/P)}', '{W/P}')
  s = s.replace('{o(W/U)o(W/U)o(W/U)o(W/U)}', '{W/U}{W/U}{W/U}{W/U}')
  s = s.replace('{o(W/U)o(W/U)}', '{W/U}{W/U}')
  s = s.replace('{o(W/U)}', '{W/U}')
  s = s.replace('{o0}', '{0}')
  s = s.replace('{o10oRoG}', '{10}{R}{G}')
  s = s.replace('{o10}', '{10}')
  s = s.replace('{o15}', '{15}')
  s = s.replace('{o1o(B/G)}', '{1}{B/G}')
  s = s.replace('{o1o(B/R)}', '{1}{B/R}')
  s = s.replace('{o1o(G/U)}', '{1}{G/U}')
  s = s.replace('{o1o(G/W)}', '{1}{G/W}')
  s = s.replace('{o1o(R/G)}', '{1}{R/G}')
  s = s.replace('{o1o(R/P)o(R/P)}', '{1}{R/P}{R/P}')
  s = s.replace('{o1o(R/W)o(R/W)}', '{1}{R/W}{R/W}')
  s = s.replace('{o1o(U/B)o(U/B)}', '{1}{U/B}{U/B}')
  s = s.replace('{o1o(U/P)o(U/P)}', '{1}{U/P}{U/P}')
  s = s.replace('{o1o(W/B)}', '{1}{W/B}')
  s = s.replace('{o1o(W/P)o(W/P)}', '{1}{W/P}{W/P}')
  s = s.replace('{o1oBoBoG}', '{1}{B}{B}{G}')
  s = s.replace('{o1oBoB}', '{1}{B}{B}')
  s = s.replace('{o1oBoG}', '{1}{B}{G}')
  s = s.replace('{o1oBoRoG}', '{1}{B}{R}{G}')
  s = s.replace('{o1oBoRoR}', '{1}{B}{R}{R}')
  s = s.replace('{o1oBoR}', '{1}{B}{R}')
  s = s.replace('{o1oB}', '{1}{B}')
  s = s.replace('{o1oC}', '{1}{C}')
  s = s.replace('{o1oGoGoG}', '{1}{G}{G}{G}')
  s = s.replace('{o1oGoG}', '{1}{G}{G}')
  s = s.replace('{o1oGoU}', '{1}{G}{U}')
  s = s.replace('{o1oGoWoU}', '{1}{G}{W}{U}')
  s = s.replace('{o1oGoW}', '{1}{G}{W}')
  s = s.replace('{o1oG}', '{1}{G}')
  s = s.replace('{o1oRoG}', '{1}{R}{G}')
  s = s.replace('{o1oRoRoW}', '{1}{R}{R}{W}')
  s = s.replace('{o1oRoR}', '{1}{R}{R}')
  s = s.replace('{o1oRoW}', '{1}{R}{W}')
  s = s.replace('{o1oR}', '{1}{R}')
  s = s.replace('{o1oSi}', '{1}{S}')
  s = s.replace('{o1oUoBoR}', '{1}{U}{B}{R}')
  s = s.replace('{o1oUoB}', '{1}{U}{B}')
  s = s.replace('{o1oUoRoW}', '{1}{U}{R}{W}')
  s = s.replace('{o1oUoR}', '{1}{U}{R}')
  s = s.replace('{o1oUoUoR}', '{1}{U}{U}{R}')
  s = s.replace('{o1oUoUoU}', '{1}{U}{U}{U}')
  s = s.replace('{o1oUoU}', '{1}{U}{U}')
  s = s.replace('{o1oU}', '{1}{U}')
  s = s.replace('{o1oWoBoG}', '{1}{W}{B}{G}')
  s = s.replace('{o1oWoB}', '{1}{W}{B}')
  s = s.replace('{o1oWoU}', '{1}{W}{U}')
  s = s.replace('{o1oWoW}', '{1}{W}{W}')
  s = s.replace('{o1oW}', '{1}{W}')
  s = s.replace('{o1}', '{1}')
  s = s.replace('{o20}', '{20}')
  s = s.replace('{o2o(B/G)o(B/G)}', '{2}{B/G}{B/G}')
  s = s.replace('{o2o(B/R)o(B/R)}', '{2}{B/R}{B/R}')
  s = s.replace('{o2o(B/R)}', '{2}{B/R}')
  s = s.replace('{o2o(G/U)o(G/U)}', '{2}{G/U}{G/U}')
  s = s.replace('{o2o(G/W)}', '{2}{G/W}')
  s = s.replace('{o2o(R/G)}', '{2}{R/G}')
  s = s.replace('{o2o(R/W)}', '{2}{R/W}')
  s = s.replace('{o2o(U/B)}', '{2}{U/B}')
  s = s.replace('{o2o(W/B)o(W/B)}', '{2}{W/B}{W/B}')
  s = s.replace('{o2o(W/U)o(W/U)}', '{2}{W/U}{W/U}')
  s = s.replace('{o2o(W/U)}', '{2}{W/U}')
  s = s.replace('{o2oBoBoG}', '{2}{B}{B}{G}')
  s = s.replace('{o2oBoB}', '{2}{B}{B}')
  s = s.replace('{o2oBoGoU}', '{2}{B}{G}{U}')
  s = s.replace('{o2oBoG}', '{2}{B}{G}')
  s = s.replace('{o2oBoRoG}', '{2}{B}{R}{G}')
  s = s.replace('{o2oBoR}', '{2}{B}{R}')
  s = s.replace('{o2oB}', '{2}{B}')
  s = s.replace('{o2oC}', '{2}{C}')
  s = s.replace('{o2oGoGoU}', '{2}{G}{G}{U}')
  s = s.replace('{o2oGoGoWoWoUoU}', '{2}{G}{G}{W}{W}{U}{U}')
  s = s.replace('{o2oGoG}', '{2}{G}{G}')
  s = s.replace('{o2oGoUoR}', '{2}{G}{U}{R}')
  s = s.replace('{o2oGoU}', '{2}{G}{U}')
  s = s.replace('{o2oGoW}', '{2}{G}{W}')
  s = s.replace('{o2oG}', '{2}{G}')
  s = s.replace('{o2oRoG}', '{2}{R}{G}')
  s = s.replace('{o2oRoRoGoG}', '{2}{R}{R}{G}{G}')
  s = s.replace('{o2oRoR}', '{2}{R}{R}')
  s = s.replace('{o2oRoWoB}', '{2}{R}{W}{B}')
  s = s.replace('{o2oRoWoW}', '{2}{R}{W}{W}')
  s = s.replace('{o2oRoW}', '{2}{R}{W}')
  s = s.replace('{o2oR}', '{2}{R}')
  s = s.replace('{o2oUoB}', '{2}{U}{B}')
  s = s.replace('{o2oUoRoW}', '{2}{U}{R}{W}')
  s = s.replace('{o2oUoR}', '{2}{U}{R}')
  s = s.replace('{o2oUoUoR}', '{2}{U}{U}{R}')
  s = s.replace('{o2oUoU}', '{2}{U}{U}')
  s = s.replace('{o2oU}', '{2}{U}')
  s = s.replace('{o2oWoBoG}', '{2}{W}{B}{G}')
  s = s.replace('{o2oWoB}', '{2}{W}{B}')
  s = s.replace('{o2oWoUoBoRoG}', '{2}{W}{U}{B}{R}{G}')
  s = s.replace('{o2oWoUoU}', '{2}{W}{U}{U}')
  s = s.replace('{o2oWoU}', '{2}{W}{U}')
  s = s.replace('{o2oWoW}', '{2}{W}{W}')
  s = s.replace('{o2oW}', '{2}{W}')
  s = s.replace('{o2}', '{2}')
  s = s.replace('{o3o(B/P)}', '{3}{B/P}')
  s = s.replace('{o3o(G/P)}', '{3}{G/P}')
  s = s.replace('{o3o(G/U)o(G/U)}', '{3}{G/U}{G/U}')
  s = s.replace('{o3o(G/W)o(G/W)}', '{3}{G/W}{G/W}')
  s = s.replace('{o3o(R/P)}', '{3}{R/P}')
  s = s.replace('{o3o(R/W)o(R/W)}', '{3}{R/W}{R/W}')
  s = s.replace('{o3o(U/P)}', '{3}{U/P}')
  s = s.replace('{o3o(W/B)}', '{3}{W/B}')
  s = s.replace('{o3o(W/P)}', '{3}{W/P}')
  s = s.replace('{o3oBoBoRoR}', '{3}{B}{B}{R}{R}')
  s = s.replace('{o3oBoB}', '{3}{B}{B}')
  s = s.replace('{o3oBoG}', '{3}{B}{G}')
  s = s.replace('{o3oBoRoG}', '{3}{B}{R}{G}')
  s = s.replace('{o3oBoR}', '{3}{B}{R}')
  s = s.replace('{o3oB}', '{3}{B}')
  s = s.replace('{o3oC}', '{3}{C}')
  s = s.replace('{o3oGoG}', '{3}{G}{G}')
  s = s.replace('{o3oGoUoR}', '{3}{G}{U}{R}')
  s = s.replace('{o3oGoU}', '{3}{G}{U}')
  s = s.replace('{o3oGoWoW}', '{3}{G}{W}{W}')
  s = s.replace('{o3oGoW}', '{3}{G}{W}')
  s = s.replace('{o3oG}', '{3}{G}')
  s = s.replace('{o3oRoGoG}', '{3}{R}{G}{G}')
  s = s.replace('{o3oRoGoW}', '{3}{R}{G}{W}')
  s = s.replace('{o3oRoG}', '{3}{R}{G}')
  s = s.replace('{o3oRoRoGoG}', '{3}{R}{R}{G}{G}')
  s = s.replace('{o3oRoRoR}', '{3}{R}{R}{R}')
  s = s.replace('{o3oRoR}', '{3}{R}{R}')
  s = s.replace('{o3oRoW}', '{3}{R}{W}')
  s = s.replace('{o3oR}', '{3}{R}')
  s = s.replace('{o3oUoBoB}', '{3}{U}{B}{B}')
  s = s.replace('{o3oUoB}', '{3}{U}{B}')
  s = s.replace('{o3oUoR}', '{3}{U}{R}')
  s = s.replace('{o3oUoU}', '{3}{U}{U}')
  s = s.replace('{o3oU}', '{3}{U}')
  s = s.replace('{o3oWoB}', '{3}{W}{B}')
  s = s.replace('{o3oWoUoBoRoG}', '{3}{W}{U}{B}{R}{G}')
  s = s.replace('{o3oWoU}', '{3}{W}{U}')
  s = s.replace('{o3oWoWoB}', '{3}{W}{W}{B}')
  s = s.replace('{o3oWoWoW}', '{3}{W}{W}{W}')
  s = s.replace('{o3oWoW}', '{3}{W}{W}')
  s = s.replace('{o3oW}', '{3}{W}')
  s = s.replace('{o3}', '{3}')
  s = s.replace('{o4o(B/G)o(B/G)}', '{4}{B/G}{B/G}')
  s = s.replace('{o4o(B/P)}', '{4}{B/P}')
  s = s.replace('{o4o(G/P)}', '{4}{G/P}')
  s = s.replace('{o4o(G/U)}', '{4}{G/U}')
  s = s.replace('{o4o(G/W)o(G/W)}', '{4}{G/W}{G/W}')
  s = s.replace('{o4o(R/G)o(R/G)}', '{4}{R/G}{R/G}')
  s = s.replace('{o4o(R/P)}', '{4}{R/P}')
  s = s.replace('{o4o(U/B)}', '{4}{U/B}')
  s = s.replace('{o4o(U/P)}', '{4}{U/P}')
  s = s.replace('{o4o(U/R)}', '{4}{U/R}')
  s = s.replace('{o4oBoBoB}', '{4}{B}{B}{B}')
  s = s.replace('{o4oBoB}', '{4}{B}{B}')
  s = s.replace('{o4oBoG}', '{4}{B}{G}')
  s = s.replace('{o4oBoR}', '{4}{B}{R}')
  s = s.replace('{o4oB}', '{4}{B}')
  s = s.replace('{o4oC}', '{4}{C}')
  s = s.replace('{o4oGoG}', '{4}{G}{G}')
  s = s.replace('{o4oGoU}', '{4}{G}{U}')
  s = s.replace('{o4oGoW}', '{4}{G}{W}')
  s = s.replace('{o4oG}', '{4}{G}')
  s = s.replace('{o4oRoG}', '{4}{R}{G}')
  s = s.replace('{o4oRoR}', '{4}{R}{R}')
  s = s.replace('{o4oRoW}', '{4}{R}{W}')
  s = s.replace('{o4oR}', '{4}{R}')
  s = s.replace('{o4oUoBoR}', '{4}{U}{B}{R}')
  s = s.replace('{o4oUoB}', '{4}{U}{B}')
  s = s.replace('{o4oUoR}', '{4}{U}{R}')
  s = s.replace('{o4oUoUoBoB}', '{4}{U}{U}{B}{B}')
  s = s.replace('{o4oUoUoR}', '{4}{U}{U}{R}')
  s = s.replace('{o4oUoU}', '{4}{U}{U}')
  s = s.replace('{o4oU}', '{4}{U}')
  s = s.replace('{o4oWoB}', '{4}{W}{B}')
  s = s.replace('{o4oWoU}', '{4}{W}{U}')
  s = s.replace('{o4oWoWoU}', '{4}{W}{W}{U}')
  s = s.replace('{o4oWoWoW}', '{4}{W}{W}{W}')
  s = s.replace('{o4oWoW}', '{4}{W}{W}')
  s = s.replace('{o4oW}', '{4}{W}')
  s = s.replace('{o4}', '{4}')
  s = s.replace('{o5o(B/P)}', '{5}{B/P}')
  s = s.replace('{o5o(R/G)o(R/G)}', '{5}{R/G}{R/G}')
  s = s.replace('{o5o(R/P)}', '{5}{R/P}')
  s = s.replace('{o5o(U/P)}', '{5}{U/P}')
  s = s.replace('{o5o(W/P)}', '{5}{W/P}')
  s = s.replace('{o5oBoBoB}', '{5}{B}{B}{B}')
  s = s.replace('{o5oBoB}', '{5}{B}{B}')
  s = s.replace('{o5oBoG}', '{5}{B}{G}')
  s = s.replace('{o5oBoR}', '{5}{B}{R}')
  s = s.replace('{o5oB}', '{5}{B}')
  s = s.replace('{o5oCoU}', '{5}{C}{U}')
  s = s.replace('{o5oGoG}', '{5}{G}{G}')
  s = s.replace('{o5oGoUoR}', '{5}{G}{U}{R}')
  s = s.replace('{o5oGoU}', '{5}{G}{U}')
  s = s.replace('{o5oG}', '{5}{G}')
  s = s.replace('{o5oRoRoR}', '{5}{R}{R}{R}')
  s = s.replace('{o5oRoR}', '{5}{R}{R}')
  s = s.replace('{o5oR}', '{5}{R}')
  s = s.replace('{o5oUoUoU}', '{5}{U}{U}{U}')
  s = s.replace('{o5oUoU}', '{5}{U}{U}')
  s = s.replace('{o5oU}', '{5}{U}')
  s = s.replace('{o5oWoB}', '{5}{W}{B}')
  s = s.replace('{o5oWoW}', '{5}{W}{W}')
  s = s.replace('{o5oW}', '{5}{W}')
  s = s.replace('{o5}', '{5}')
  s = s.replace('{o6o(B/P)}', '{6}{B/P}')
  s = s.replace('{o6o(G/U)o(G/U)}', '{6}{G/U}{G/U}')
  s = s.replace('{o6o(G/W)}', '{6}{G/W}')
  s = s.replace('{o6o(W/P)}', '{6}{W/P}')
  s = s.replace('{o6oB}', '{6}{B}')
  s = s.replace('{o6oGoGoG}', '{6}{G}{G}{G}')
  s = s.replace('{o6oGoG}', '{6}{G}{G}')
  s = s.replace('{o6oG}', '{6}{G}')
  s = s.replace('{o6oRoG}', '{6}{R}{G}')
  s = s.replace('{o6oRoRoR}', '{6}{R}{R}{R}')
  s = s.replace('{o6oRoR}', '{6}{R}{R}')
  s = s.replace('{o6oRoW}', '{6}{R}{W}')
  s = s.replace('{o6oR}', '{6}{R}')
  s = s.replace('{o6oUoUoU}', '{6}{U}{U}{U}')
  s = s.replace('{o6oUoU}', '{6}{U}{U}')
  s = s.replace('{o6oU}', '{6}{U}')
  s = s.replace('{o6oWoB}', '{6}{W}{B}')
  s = s.replace('{o6oWoW}', '{6}{W}{W}')
  s = s.replace('{o6}', '{6}')
  s = s.replace('{o7oBoBoB}', '{7}{B}{B}{B}')
  s = s.replace('{o7oB}', '{7}{B}')
  s = s.replace('{o7oGoGoG}', '{7}{G}{G}{G}')
  s = s.replace('{o7oGoG}', '{7}{G}{G}')
  s = s.replace('{o7oG}', '{7}{G}')
  s = s.replace('{o7oR}', '{7}{R}')
  s = s.replace('{o7oUoU}', '{7}{U}{U}')
  s = s.replace('{o7oU}', '{7}{U}')
  s = s.replace('{o7oW}', '{7}{W}')
  s = s.replace('{o7}', '{7}')
  s = s.replace('{o8oRoR}', '{8}{R}{R}')
  s = s.replace('{o8oR}', '{8}{R}')
  s = s.replace('{o8oU}', '{8}{U}')
  s = s.replace('{o8}', '{8}')
  s = s.replace('{o9o(G/P)}', '{9}{G/P}')
  s = s.replace('{o9}', '{9}')
  s = s.replace('{oBoBoBoB}', '{B}{B}{B}{B}')
  s = s.replace('{oBoBoB}', '{B}{B}{B}')
  s = s.replace('{oBoBoRoR}', '{B}{B}{R}{R}')
  s = s.replace('{oBoB}', '{B}{B}')
  s = s.replace('{oBoGoU}', '{B}{G}{U}')
  s = s.replace('{oBoG}', '{B}{G}')
  s = s.replace('{oBoRoG}', '{B}{R}{G}')
  s = s.replace('{oBoR}', '{B}{R}')
  s = s.replace('{oB}', '{B}')
  s = s.replace('{oCoCoCoCoC}', '{C}{C}{C}{C}{C}')
  s = s.replace('{oCoCoC}', '{C}{C}{C}')
  s = s.replace('{oCoCoR}', '{C}{C}{R}')
  s = s.replace('{oCoC}', '{C}{C}')
  s = s.replace('{oCoU}', '{C}{U}')
  s = s.replace('{oCoWoUoBoRoG}', '{C}{W}{U}{B}{R}{G}')
  s = s.replace('{oC}', '{C}')
  s = s.replace('{oEoEoEoEoE}', '{E}{E}{E}{E}{E}')
  s = s.replace('{oEoEoEoE}', '{E}{E}{E}{E}')
  s = s.replace('{oEoEoE}', '{E}{E}{E}')
  s = s.replace('{oEoE}', '{E}{E}')
  s = s.replace('{oE}', '{E}')
  s = s.replace('{oGoGoGoGoG}', '{G}{G}{G}{G}{G}')
  s = s.replace('{oGoGoGoG}', '{G}{G}{G}{G}')
  s = s.replace('{oGoGoG}', '{G}{G}{G}')
  s = s.replace('{oGoGoUoU}', '{G}{G}{U}{U}')
  s = s.replace('{oGoG}', '{G}{G}')
  s = s.replace('{oGoUoR}', '{G}{U}{R}')
  s = s.replace('{oGoU}', '{G}{U}')
  s = s.replace('{oGoWoU}', '{G}{W}{U}')
  s = s.replace('{oGoWoW}', '{G}{W}{W}')
  s = s.replace('{oGoW}', '{G}{W}')
  s = s.replace('{oG}', '{G}')
  s = s.replace('{oHoHoH}', '{P}{P}{P}')
  s = s.replace('{oHoH}', '{P}{P}')
  s = s.replace('{oH}', '{P}')
  s = s.replace('{oRoGoWoU}', '{R}{G}{W}{U}')
  s = s.replace('{oRoGoW}', '{R}{G}{W}')
  s = s.replace('{oRoG}', '{R}{G}')
  s = s.replace('{oRoRoRoGoGoG}', '{R}{R}{R}{G}{G}{G}')
  s = s.replace('{oRoRoRoRoR}', '{R}{R}{R}{R}{R}')
  s = s.replace('{oRoRoRoR}', '{R}{R}{R}{R}')
  s = s.replace('{oRoRoR}', '{R}{R}{R}')
  s = s.replace('{oRoRoWoW}', '{R}{R}{W}{W}')
  s = s.replace('{oRoR}', '{R}{R}')
  s = s.replace('{oRoWoB}', '{R}{W}{B}')
  s = s.replace('{oRoW}', '{R}{W}')
  s = s.replace('{oR}', '{R}')
  s = s.replace('{oSioSioSioSi}', '{S}{S}{S}{S}')
  s = s.replace('{oSioSioSi}', '{S}{S}{S}')
  s = s.replace('{oSioSi}', '{S}{S}')
  s = s.replace('{oSi}', '{S}')
  s = s.replace('{oT}', '{T}')
  s = s.replace('{oUoBoR}', '{U}{B}{R}')
  s = s.replace('{oUoB}', '{U}{B}')
  s = s.replace('{oUoRoW}', '{U}{R}{W}')
  s = s.replace('{oUoR}', '{U}{R}')
  s = s.replace('{oUoUoRoRoR}', '{U}{U}{R}{R}{R}')
  s = s.replace('{oUoUoU}', '{U}{U}{U}')
  s = s.replace('{oUoU}', '{U}{U}')
  s = s.replace('{oU}', '{U}')
  s = s.replace('{oWoBoG}', '{W}{B}{G}')
  s = s.replace('{oWoB}', '{W}{B}')
  s = s.replace('{oWoUoBoRoG}', '{W}{U}{B}{R}{G}')
  s = s.replace('{oWoUoB}', '{W}{U}{B}')
  s = s.replace('{oWoU}', '{W}{U}')
  s = s.replace('{oWoWoB}', '{W}{W}{B}')
  s = s.replace('{oWoWoUoUoBoBoRoRoGoG}', '{W}{W}{U}{U}{B}{B}{R}{R}{G}{G}')
  s = s.replace('{oWoWoWoWoW}', '{W}{W}{W}{W}{W}')
  s = s.replace('{oWoWoW}', '{W}{W}{W}')
  s = s.replace('{oWoW}', '{W}{W}')
  s = s.replace('{oW}', '{W}')
  s = s.replace('{oXo(B/G)}', '{X}{B/G}')
  s = s.replace('{oXo1oU}', '{X}{1}{U}')
  s = s.replace('{oXo2oR}', '{X}{2}{R}')
  s = s.replace('{oXo2oW}', '{X}{2}{W}')
  s = s.replace('{oXo3oW}', '{X}{3}{W}')
  s = s.replace('{oXoBoB}', '{X}{B}{B}')
  s = s.replace('{oXoB}', '{X}{B}')
  s = s.replace('{oXoGoGoGoG}', '{X}{G}{G}{G}{G}')
  s = s.replace('{oXoGoGoU}', '{X}{G}{G}{U}')
  s = s.replace('{oXoGoG}', '{X}{G}{G}')
  s = s.replace('{oXoG}', '{X}{G}')
  s = s.replace('{oXoRoG}', '{X}{R}{G}')
  s = s.replace('{oXoRoRoR}', '{X}{R}{R}{R}')
  s = s.replace('{oXoRoW}', '{X}{R}{W}')
  s = s.replace('{oXoR}', '{X}{R}')
  s = s.replace('{oXoUoUoBoB}', '{X}{U}{U}{B}{B}')
  s = s.replace('{oXoUoU}', '{X}{U}{U}')
  s = s.replace('{oXoU}', '{X}{U}')
  s = s.replace('{oXoWoUoU}', '{X}{W}{U}{U}')
  s = s.replace('{oXoW}', '{X}{W}')
  s = s.replace('{oXoXoB}', '{X}{X}{B}')
  s = s.replace('{oXoXoGoG}', '{X}{X}{G}{G}')
  s = s.replace('{oXoXoG}', '{X}{X}{G}')
  s = s.replace('{oXoXoW}', '{X}{X}{W}')
  s = s.replace('{oXoX}', '{X}{X}')
  s = s.replace('{oX}', '{X}')

  #x = re.findall("{o.*?}", s)
  #if len(x) > 0:
  #  print(f"REGEX = {x}")
  return s
