import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Form, Input, Button, Card, message } from 'antd';
import { useAuth } from '../../contexts/AuthContext';
import '../../styles/auth/Register.css';

const Register = () => {
    const [loading, setLoading] = useState(false);
    const { register } = useAuth();
    const navigate = useNavigate();

    const onFinish = async (values) => {
        setLoading(true);
        try {
            await register(values.email, values.firstname, values.lastname);
            message.success('Registration successful! You can now login.');
            navigate('/login');
        } catch (error) {
            message.error(error.response?.data?.error || 'Registration failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <Card className="register-card" title="Register">
                <Form
                    name="register"
                    onFinish={onFinish}
                    layout="vertical"
                    autoComplete="off"
                >
                    <Form.Item
                        label="First Name"
                        name="firstname"
                        rules={[{ required: true, message: 'Please input your first name!' }]}
                    >
                        <Input placeholder="Enter your first name" />
                    </Form.Item>

                    <Form.Item
                        label="Last Name"
                        name="lastname"
                        rules={[{ required: true, message: 'Please input your last name!' }]}
                    >
                        <Input placeholder="Enter your last name" />
                    </Form.Item>

                    <Form.Item
                        label="Email"
                        name="email"
                        rules={[
                            { required: true, message: 'Please input your email!' },
                            { type: 'email', message: 'Please enter a valid email!' }
                        ]}
                    >
                        <Input placeholder="Enter your email" />
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" htmlType="submit" loading={loading} block>
                            Register
                        </Button>
                    </Form.Item>

                    <div className="register-footer">
                        <Link to="/login">Already have an account? Login</Link>
                    </div>
                </Form>
            </Card>
        </div>
    );
};

export default Register;

