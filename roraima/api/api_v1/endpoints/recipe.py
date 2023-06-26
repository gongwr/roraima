from fastapi import APIRouter, HTTPException, Query
from typing import Any, Optional

from roraima import crud
from roraima.db.schemas import Recipe, RecipeCreate, RecipeSearchResults

router = APIRouter()


@router.get("/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(
    *,
    recipe_id: int,
) -> Any:
    """
    Fetch a single recipe by ID
    """
    result = crud.recipe.get(id=recipe_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found"
        )

    return result


@router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10,
) -> dict:
    """
    Search for recipes based on label keyword
    """
    recipes = crud.recipe.get_multi(limit=max_results)
    if not keyword:
        return {"results": recipes}

    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)
    return {"results": list(results)[:max_results]}


@router.post("/", status_code=201, response_model=Recipe)
def create_recipe(
    *, recipe_in: RecipeCreate
) -> dict:
    """
    Create a new recipe in the database.
    """
    recipe = crud.recipe.create(obj_in=recipe_in)

    return recipe
