from sqlalchemy import exc

from app import db
from app.models import Recipe, Ingredient, NormalizedIngredient


def get_cocktail_recipe(id):
    recipe = Recipe.query.get(id)
    return recipe



def get_normalized_ingredient(id, name):
    ingredient = NormalizedIngredient.query.get(id)
    if ingredient:
        return ingredient
    else:
        ingredient = NormalizedIngredient(id=id, name=name)
        db.session.add(ingredient)
        db.session.commit()
        return ingredient




def get_ingredient(id, name, normalized_id, normalized_name):
    ingredient = Ingredient.query.get(id)
    if ingredient:
        return ingredient
    else:
        ingredient = Ingredient(id=id, name=name,
                                normalized=get_normalized_ingredient(id=normalized_id,
                                                                     name=normalized_name)
                                )
        db.session.add(ingredient)
        db.session.commit()
        return ingredient



def add_cocktail_recipe_cb(name, url, instructions, ingredients):
    new_recipe = Recipe()
    new_recipe.name = name
    new_recipe.cb_url = url
    new_recipe.instructions = instructions
    new_recipe.ingredients = [get_ingredient(id=ingredient["ID"], name=ingredient["Name"],
                                             normalized_id=ingredient["NormalizedID"],
                                             normalized_name=ingredient["NormalizedName"]
                                             ) for ingredient in ingredients]
    new_recipe.amounts = [{"amount": ingredient["Amount"], "measurement": ingredient["Measurement"],
                           "id": ingredient["ID"], "name": ingredient["Name"]} for ingredient in ingredients]
    new_recipe.amounts_str = "\n".join(["{} {} {}".format(ingredient["Amount"], ingredient["Measurement"],
                                                          ingredient["Name"])
                                        for ingredient in ingredients])
    new_recipe.rating = -1

    try:
        db.session.add(new_recipe)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return False
    else:
        return True


def set_rating(id, rating_num):
    recipe = Recipe.query.get(id)
    if not recipe:
        return False
    recipe.rating = rating_num
    db.session.commit()
    return True
