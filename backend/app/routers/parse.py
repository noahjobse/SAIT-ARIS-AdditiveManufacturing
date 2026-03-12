"""
Parse endpoint — accepts raw RAPID code, returns parsed AST.
"""
import dataclasses

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.parser.parser import RapidParseError, RapidParser

router = APIRouter()
_parser = RapidParser()


def _to_dict(obj):
    """Recursively convert dataclasses to dicts for JSON serialization."""
    if dataclasses.is_dataclass(obj):
        return {k: _to_dict(v) for k, v in dataclasses.asdict(obj).items()}
    if isinstance(obj, list):
        return [_to_dict(i) for i in obj]
    return obj


class ParseRequest(BaseModel):
    code: str


class ParseResponse(BaseModel):
    module_count: int
    command_count: int
    program: dict


@router.post("/api/parse", response_model=ParseResponse)
async def parse_rapid(request: ParseRequest):
    """
    Parse RAPID source code and return the AST.

    Raises 400 if the code has syntax errors.
    """
    try:
        program = _parser.parse(request.code)
    except RapidParseError as e:
        raise HTTPException(status_code=400, detail=e.message)

    command_count = sum(
        len(proc.commands)
        for module in program.modules
        for proc in module.procedures
    )

    return ParseResponse(
        module_count=len(program.modules),
        command_count=command_count,
        program=_to_dict(program),
    )
