const express = require('express');
const Router = express.Router({mergeParams:true});
const WrapperAsync = require('../utils/WrapperAsync')
const ExpressError = require('../utils/ExpressError')
const {isLoggedIn, ValidateReview, isReviewOwner} = require('../middleware');
const Controller = require('../controllers/review');


Router.post('/',isLoggedIn,ValidateReview,WrapperAsync(Controller.newReview));

Router.delete('/:reviewid',isLoggedIn,isReviewOwner,WrapperAsync(Controller.deleteReview));

module.exports = Router;