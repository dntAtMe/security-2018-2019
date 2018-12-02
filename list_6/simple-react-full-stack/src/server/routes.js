module.exports = function(app, passport) {

    app.get('/api/ping', checkAuth, (req, res) => {
        res.send({username: req.user});
    });

    app.get('/api/zwei', (req, res) => res.send({ username: "zwei" }));

    function checkAuth(req, res, next) {
        if (req.isAuthenticated()) {
            return next();
        }
        res.redirect('/');
    }
    app.get('/api/signup', (req, res) => res.send({ username: "signup" }));

    app.post('/api/signup', passport.authenticate('local-signup', {
		successRedirect : '/api/ping', // redirect to the secure profile section
		failureRedirect : '/api/zwei', // redirect back to the signup page if there is an error
}));
}