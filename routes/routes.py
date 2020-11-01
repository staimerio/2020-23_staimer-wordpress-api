# Retic
from retic import Router

# Controllers
import controllers.wordpress as wordpress

"""Define Router instance"""
router = Router()

"""Define all paths - posts"""
router \
    .post("/posts", wordpress.create_post) \
    .get("/posts", wordpress.get_all_search) \

"""Define all paths - posts/:post_id"""
router \
    .get("/posts/:post_id", wordpress.get_post_by_id) \
    .put("/posts/:post_id", wordpress.update_post)
