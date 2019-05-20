require('./croppie');
// RENDER TEMPLATES
const user = require('./user');
const recipe = require('./recipe');
const comment = require('./comment');
const utils = require('./utils');



// ----------------------------------------------------------------------------- EXPORTS
exports.signupUser = user.signupUser;
exports.logInUser = user.logInUser;
exports.getUserRecipes = user.getUserRecipes;
exports.getUserData = user.getUserData;
exports.getUserFavorites = user.getUserFavorites;
exports.updateUserData = user.updateUserData;
exports.addRecipe = recipe.addRecipe;
exports.updateRecipe = recipe.updateRecipe;
exports.deleteRecipe = recipe.deleteRecipe;
exports.getRecipes = recipe.getRecipes;
exports.addRecipeLine = recipe.addRecipeLine;
exports.removeRecipeLine = recipe.removeRecipeLine;
exports.postComment = comment.postComment;
exports.deleteComment = comment.deleteComment;
exports.toggleFavorite = utils.toggleFavorite;
exports.updateRating = utils.updateRating;

