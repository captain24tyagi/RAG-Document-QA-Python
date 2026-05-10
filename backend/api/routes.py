# api/routes.py

# api/routes.py

# from fastapi import APIRouter, UploadFile, File, HTTPException
# from api.models import QuestionRequest, QuestionResponse, IngestResponse
# from services.injest_service import ingest_document
# from services.qa_service import answer_question
# from core.parser import extract_text, SUPPORTED_EXTENSIONS

# router = APIRouter()



# @router.post("/ingest", response_model=IngestResponse)
# async def ingest(file: UploadFile = File(...)):
#     """
#     Upload a document (.txt, .pdf, .docx) and ingest it into the vector store.

#     Accepts: multipart/form-data with a file field
#     Returns: { message, chunks_stored, new_chunks }
#     """
#     # Validate extension
#     filename = file.filename or ""
#     ext = f".{filename.rsplit('.', 1)[-1].lower()}" if "." in filename else ""

#     if ext not in SUPPORTED_EXTENSIONS:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Unsupported file type '{ext}'. Allowed: .txt, .pdf, .docx"
#         )

#     content = await file.read()

#     if not content:
#         raise HTTPException(status_code=400, detail="Uploaded file is empty.")

#     # Extract text based on file type
#     try:
#         text = extract_text(content, filename)
#     except ValueError as e:
#         raise HTTPException(status_code=422, detail=str(e))

#     if not text.strip():
#         raise HTTPException(status_code=400, detail="No text could be extracted from the document.")

#     result = ingest_document(text)

#     return IngestResponse(
#         message="Document ingested successfully.",
#         chunks_stored=result["chunks_stored"],
#         new_chunks=result["new_chunks"]
#     )


# @router.post("/ask", response_model=QuestionResponse)
# async def ask(request: QuestionRequest):
#     """
#     Ask a question against the uploaded document.

#     Body: { "query": str, "top_k": int (optional, default 5) }
#     Returns: { "answer": str, "source_chunks": [...] }
#     """
#     if not request.query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     result = answer_question(request.query, top_k=request.top_k)
#     return result


# @router.post("/ask", response_model=QuestionResponse)
# async def ask(request: QuestionRequest):
#     """
#     Ask a question against the uploaded document.
    
#     Body: { "query": str, "top_k": int (optional, default 5) }
#     Returns: { "answer": str, "source_chunks": [...] }
#     """
#     if not request.query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     result = answer_question(request.query, top_k=request.top_k)
#     return result

from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from api.models import QuestionResponse, QuestionRequest, IngestResponse
from services.injest_service import ingest_document
from services.qa_service import answer_question
from core.parser import extract_text, SUPPORTED_EXTENSIONS
from middleware.rate_limiter import limiter

router = APIRouter()

MAX_FILE_SIZE = 20 * 1024 * 1024

@router.post("/ingest", response_model=IngestResponse)
@limiter.limit("2/minute")   
async def ingest(request: Request,file: UploadFile = File(...)):

    """
    Upload a document (.txt, .pdf, .docx) and ingest it into the vector store.

    Accepts: multipart/form-data with a file field
    Returns: { message, chunks_stored, new_chunks }
    """
    # Validate extension

    filename = file.filename or ""
    ext = f".{filename.rsplit('.', 1)[-1].lower()}" if "." in filename else ""

    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum allowed size is 20MB."
        )

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        text = extract_text(content, filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    if not text.strip():
        raise  HTTPException(status_code=400, detail="No text could be extracted from the document.")

    result = ingest_document(text)

    return IngestResponse(
        message="Document ingested successfully.",
        chunks_stored=result["chunks_stored"],
        new_chunks=result["new_chunks"]
    )

@router.post("/ask", response_model=QuestionResponse)
@limiter.limit("3/minute") 
async def ask(request: Request, body: QuestionRequest):    
    """
    Ask a question against the uploaded document.
    
    Body: { "query": str, "top_k": int (optional, default 5) }
    Returns: { "answer": str, "source_chunks": [...] }
    """

    if not body.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    result = answer_question(body.query, top_k=body.top_k)
    return result