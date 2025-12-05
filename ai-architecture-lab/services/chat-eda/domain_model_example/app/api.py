"""
API Layer (Beginner-Friendly Explanation)
========================================

This file contains the FastAPI **HTTP routing layer** for the Domain Model example.

Architecture Summary
--------------------
We now have THREE separate layers working together:

1. API Layer (this file)
   - Receives HTTP requests from the client
   - Converts them into domain operations
   - Converts domain objects back into JSON using Pydantic
   - Contains *no business rules* and *no SQL*

2. Domain Model (domain.py)
   - Holds the core business logic
   - Defines what a Conversation *is* and *can do*
   - Enforces rules like:
         “you cannot add messages after a conversation is closed”
   - Represents rich domain behavior — not just data containers

3. Repository (repository.py)
   - Handles saving/loading to SQLite
   - Translates between Python domain objects and database rows
   - Keeps persistence logic out of the domain and API layers

Why this matters for beginners:
-------------------------------
This small example shows an important real-world pattern:
**each layer has exactly ONE responsibility.**

- API layer: orchestrates requests
- Domain model: business logic / behavior
- Repository: persistence

This gives us:
- Testable code
- Reusable domain logic (could be used in CLI, jobs, AI pipelines)
- Maintainable structure
- Clean separation between HTTP, business rules, and database
"""

import os
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .domain import Conversation
from .repository import ConversationRepository


# -------------------------------------------------------------------
# DATABASE CONFIGURATION
# -------------------------------------------------------------------
# The API layer does NOT talk directly to SQLite.
# Instead, we construct a Repository that handles all DB operations.
#
# Setting DB_PATH allows tests to run against an isolated temporary file.
# Example for tests:
#       DB_PATH=/tmp/test.db pytest
DB_PATH = os.getenv("DB_PATH", "./conversations.db")
repo = ConversationRepository(DB_PATH)


# -------------------------------------------------------------------
# FASTAPI APPLICATION INITIALIZATION
# -------------------------------------------------------------------
app = FastAPI(title="Chat Domain Model Demo")


# -------------------------------------------------------------------
# REQUEST/RESPONSE MODELS (Pydantic DTOs)
# -------------------------------------------------------------------
# Pydantic is used ONLY for API input/output.
# Domain objects remain clean and independent of FastAPI/Pydantic.
class ConversationIn(BaseModel):
    title: str


class MessageIn(BaseModel):
    sender: str
    text: str


class MessageOut(BaseModel):
    sender: str
    text: str
    created_at: str


class ConversationOut(BaseModel):
    id: int
    title: str
    closed: bool
    messages: List[MessageOut]


# -------------------------------------------------------------------
# HELPER: Convert domain Conversation → Pydantic ConversationOut
# -------------------------------------------------------------------
def _conv_to_out(conv: Conversation) -> ConversationOut:
    """
    Converts a *domain* Conversation object into a *Pydantic* API response.

    API layer uses Pydantic → Domain layer uses dataclasses.
    This translation step is normal in layered architecture.
    """
    return ConversationOut(
        id=conv.id,
        title=conv.title,
        closed=conv.closed,
        messages=[
            MessageOut(sender=m.sender, text=m.text, created_at=m.created_at)
            for m in conv.messages
        ],
    )


# ===================================================================
# ENDPOINT: CREATE A NEW CONVERSATION
# ===================================================================
@app.post("/conversations", response_model=ConversationOut)
def create_conversation(payload: ConversationIn):
    """
    Create a new conversation.

    Flow:
    - Create a domain object
    - Save it using the Repository
    - Return the converted Pydantic response

    Domain logic (none yet) stays inside Conversation.
    SQL stays inside the Repository.
    """
    conv = Conversation(title=payload.title)
    saved = repo.save(conv)
    return _conv_to_out(saved)


# ===================================================================
# ENDPOINT: GET ONE CONVERSATION BY ID
# ===================================================================
@app.get("/conversations/{conv_id}", response_model=ConversationOut)
def get_conversation(conv_id: int):
    """
    Retrieve a single conversation by ID.

    Notice:
    - No SQL here
    - No business logic here
    - All heavy lifting happens in the Repo + Domain
    """
    conv = repo.get(conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="conversation not found")
    return _conv_to_out(conv)


# ===================================================================
# ENDPOINT: ADD A MESSAGE TO A CONVERSATION
# ===================================================================
@app.post("/conversations/{conv_id}/messages", response_model=ConversationOut)
def add_message(conv_id: int, payload: MessageIn):
    """
    Add a new message to the conversation.

    IMPORTANT:
    - The domain model enforces rules such as:
          “cannot add messages to a closed conversation”
    - If a domain rule is violated, we catch the error
      and convert it into a proper HTTP response.

    This is the value of putting logic in the Domain Model.
    """
    conv = repo.get(conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="conversation not found")

    try:
        conv.add_message(payload.sender, payload.text)
    except ValueError as e:
        # Domain rule violation → translate into HTTP 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))

    repo.save(conv)
    return _conv_to_out(conv)


# ===================================================================
# ENDPOINT: CLOSE A CONVERSATION
# ===================================================================
@app.post("/conversations/{conv_id}/close", response_model=ConversationOut)
def close_conversation(conv_id: int):
    """
    Mark the conversation as closed.

    After closing:
    - You cannot add new messages
    - This rule exists *inside the domain model*, not the API

    This endpoint simply delegates to:
      - Domain logic (conv.close())
      - Repository persistence (repo.save())
    """
    conv = repo.get(conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="conversation not found")

    conv.close()
    repo.save(conv)
    return _conv_to_out(conv)
