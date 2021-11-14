if (process.env.NODE_ENV !== "production") {
    require('dotenv').config();
}

const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const CampRouter = require('./routes/campgrounds');
const ReviewRouter = require('./routes/reviews')
const UserRouter = require('./routes/users');
const methods = require('method-override');
const ejsMate = require('ejs-mate');
const ExpressError = require('./utils/ExpressError')
const session = require('express-session');
const flash = require('express-flash');
const passportLocal = require('passport-local');
const passport = require('passport');
const User = require('./models/Usermodel');
const mongoSanitize = require('express-mongo-sanitize')
const helmet = require('helmet');
const MongoStore = require('connect-mongo');
const mongoUrl = process.env.mongoUrl;
const favicon = path.join(__dirname, 'favicon.ico');
const Mongostore = require('connect-mongo');
// 'mongodb://localhost:27017/Yelp'
const connect = mongoose.connect(mongoUrl);
const db = mongoose.connection;

db.on('error', console.error.bind(console, 'connection error'));
db.once('open', () => {
    console.log('Database Connected');
})


const app = express();

app.engine('ejs', ejsMate);
app.use(express.urlencoded({ extended: true }));
app.use(methods('_method'));
app.use(express.static('public'));
app.use(
    mongoSanitize({
        replaceWith: '_',
    }),
);

app.use(helmet());


const scriptSrcUrls = [
    "https://stackpath.bootstrapcdn.com/",
    "https://api.tiles.mapbox.com/",
    "https://api.mapbox.com/",
    "https://kit.fontawesome.com/",
    "https://cdnjs.cloudflare.com/",
    "https://cdn.jsdelivr.net",
];
const styleSrcUrls = [
    "https://kit-free.fontawesome.com/",
    "https://stackpath.bootstrapcdn.com/",
    "https://api.mapbox.com/",
    "https://api.tiles.mapbox.com/",
    "https://fonts.googleapis.com/",
    "https://use.fontawesome.com/",
    "https://cdn.jsdelivr.net/"
];
const connectSrcUrls = [
    "https://api.mapbox.com/",
    "https://a.tiles.mapbox.com/",
    "https://b.tiles.mapbox.com/",
    "https://events.mapbox.com/",
];
const fontSrcUrls = [];
app.use(
    helmet.contentSecurityPolicy({
        directives: {
            defaultSrc: [],
            connectSrc: ["'self'", ...connectSrcUrls],
            scriptSrc: ["'unsafe-inline'", "'self'", ...scriptSrcUrls],
            styleSrc: ["'self'", "'unsafe-inline'", ...styleSrcUrls],
            workerSrc: ["'self'", "blob:"],
            objectSrc: [],
            imgSrc: [
                "'self'",
                "blob:",
                "data:",
                "https://res.cloudinary.com/dvl0tpsdb/",
                "https://images.unsplash.com/",
                "https://source.unsplash.com/"

            ],
            fontSrc: ["'self'", ...fontSrcUrls],
        },
    })
);

const store = Mongostore.create({
    mongoUrl,
    touchAfter: 24 * 60 * 60
})

store.on('error', function(e) {
    console.log("Session store error", e);
})

const secret = process.env.session_secret
const sessionConfig = {
    store,
    name: 'notso',
    secret,
    resave: false,
    saveUninitialized: true,
    SameSite: 'strict',
    MaxAge: 1000 * 60 * 60 * 24,
    HttpOnly: true
}
app.use(session(sessionConfig));
app.use(flash());
app.use(passport.initialize());
app.use(passport.session());
passport.use(new passportLocal(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

app.use((req, res, next) => {
    res.locals.currentUser = req.user;
    res.locals.success = req.flash('success');
    res.locals.error = req.flash('error');
    next();
})

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, "views"));

app.get('/', (req, res) => {
    res.render('home');
})
app.get('/favicon.ico', (req, res) => {
    res.sendFile(favicon);
})
app.use('/', UserRouter);
app.use('/campgrounds', CampRouter);
app.use('/campgrounds/:campid/reviews', ReviewRouter);

app.all('*', (req, res, next) => {
    // console.dir(req);
    next(new ExpressError("These arent the droids you are looking for!", 404))
})

app.use((err, req, res, next) => {
    console.dir(err);
    res.render('error', { err });
})

const port = process.env.PORT || 8080
app.listen(port, () => {
    console.log(`Port: ${port}`);
})