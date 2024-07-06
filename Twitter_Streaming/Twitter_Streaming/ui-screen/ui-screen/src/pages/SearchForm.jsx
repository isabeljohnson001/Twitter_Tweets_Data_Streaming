import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';


/* This is the search page */
const SearchForm = ({ initialSearchTerm }) => {
    const [searchTerm, setSearchTerm] = useState(initialSearchTerm || '');
    const navigate = useNavigate();

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleSearchSubmit = (event) => {
        event.preventDefault();
        navigate(`/tweets/${searchTerm}`);
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSearchSubmit(event);
        }
      };

    return (
        <form onSubmit={handleSearchSubmit} className="search-form">
            <input
                type="text"
                className="search-input"
                value={searchTerm}
                onChange={handleSearchChange}
                placeholder="Search..."
            />
            <button type="submit" className="search-button">Search</button>
        </form>
    );
};

export default SearchForm;
