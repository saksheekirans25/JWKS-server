const request = require('supertest');
const app = require('../app'); // Adjust the path if necessary

describe('POST /auth', () => {
    it('should return a valid JWT', async () => {
        const response = await request(app)
            .post('/auth')
            .send({ username: 'helloworld', password: 'hellohello' })
            .set('Accept', 'application/json');

        expect(response.status).toBe(200);
        expect(response.body.token).toBeDefined();
    });

    it('should return a 400 for missing credentials', async () => {
        const response = await request(app)
            .post('/auth')
            .send({})
            .set('Accept', 'application/json');

        expect(response.status).toBe(400); // Assuming your API returns 400 for bad requests
    });
});
