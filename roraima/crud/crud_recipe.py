from roraima.crud.base import CRUDBase
from roraima.db.models import Recipe
from roraima.db.schemas import RecipeCreate, RecipeUpdate


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    ...


recipe = CRUDRecipe(Recipe)
