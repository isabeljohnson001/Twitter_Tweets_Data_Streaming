import React from 'react';
import SearchForm from './SearchForm';
import '../App.css';
import { Outlet } from 'react-router-dom';


/* This is the home page */
const Home = () => {
    return (
        <div className="home">
            <h1>Twitter Tweet Analysis</h1>
            <SearchForm />
            <Outlet /> {/* Renders child components based on the route */}
        </div>
    );
};

export default Home;
