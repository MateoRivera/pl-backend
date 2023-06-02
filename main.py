from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import numpy as np

from simplex_calculator import solve

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProblemStatement(BaseModel):
    c: list  # Objective function
    # Coefficients of the inequalities (left-hand side and less-than-or-equal-to <=)
    A_ub: list
    # Coefficients of the equalities (left-hand side and equal-to ==)
    A_eq: list
    # Right-hand side of the inequalities (right-hand side and less-than-or-equal-to <=)
    b_ub: list
    # Right-hand side of the equalities (right-hand side and equal-to ==)
    b_eq: list


@app.post("/solve")
async def resolve_problem_statement(req: ProblemStatement):
    print(req)
    c = np.array(req.c)
    return solve(c, req.A_ub, req.b_ub, req.A_eq, req.b_eq)
