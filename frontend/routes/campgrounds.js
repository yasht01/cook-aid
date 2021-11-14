const express = require('express')
const Router = express.Router()
const WrapperAsync = require('../utils/WrapperAsync')
const {isLoggedIn, ValidateCamp,ValidateId,isOwner} = require('../middleware');
const Controller = require('../controllers/campground')
const multer = require('multer');
const { storage } = require('../cloudinary');
const upload = multer({ storage });

Router.route('/')
    .get(WrapperAsync(Controller.index))
    // .post(WrapperAsync(Controller.createCampground))
    .post(isLoggedIn,upload.array('images'),ValidateCamp,WrapperAsync(Controller.createCampground));

Router.get('/new',isLoggedIn,Controller.newForm);
    
Router.route('/:id')
    .get(ValidateId ,WrapperAsync(Controller.renderDetails))
    .post(isLoggedIn,upload.array('images'),ValidateCamp,isOwner,WrapperAsync(Controller.editCampground))
    .delete(isLoggedIn,isOwner,WrapperAsync(Controller.deleteCampground));

Router.get('/:id/edit',isLoggedIn,isOwner,WrapperAsync(Controller.renderEditForm));


module.exports = Router;