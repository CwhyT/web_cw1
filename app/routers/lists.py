from fastapi import APIRouter

router = APIRouter(prefix="/lists", tags=["lists"])


@router.post("")
def create_list_placeholder() -> dict[str, str]:
    return {"message": "Create reading list placeholder"}


@router.get("")
def list_lists_placeholder() -> dict[str, list]:
    return {"items": []}


@router.get("/{list_id}")
def get_list_placeholder(list_id: int):
    return {"list_id": list_id, "message": "Get reading list placeholder"}


@router.put("/{list_id}")
def update_list_placeholder(list_id: int):
    return {"list_id": list_id, "message": "Update reading list placeholder"}


@router.delete("/{list_id}")
def delete_list_placeholder(list_id: int):
    return {"list_id": list_id, "message": "Delete reading list placeholder"}


@router.post("/{list_id}/items")
def add_list_item_placeholder(list_id: int):
    return {"list_id": list_id, "message": "Add book to reading list placeholder"}


@router.put("/{list_id}/items/{item_id}")
def update_list_item_placeholder(list_id: int, item_id: int):
    return {
        "list_id": list_id,
        "item_id": item_id,
        "message": "Update reading list item placeholder",
    }


@router.delete("/{list_id}/items/{item_id}")
def delete_list_item_placeholder(list_id: int, item_id: int):
    return {
        "list_id": list_id,
        "item_id": item_id,
        "message": "Delete reading list item placeholder",
    }

