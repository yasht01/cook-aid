const express = require('express');
const Router = express.Router();
const { ValidateUser } = require('../middleware');
const passport = require('passport');
const Controller = require('../controllers/user');


Router.route('/register')
    .get(Controller.registerForm)
    .post(ValidateUser, Controller.registerUser);

Router.route('/login')
    .get(Controller.loginForm)
    .post(passport.authenticate('local', { failureFlash: true, failureRedirect: '/login' }), Controller.loginUser);

Router.get('/logout', Controller.logoutUser);

module.exports = Router;