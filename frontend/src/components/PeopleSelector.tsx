import React, { useState, useCallback, useEffect, useMemo } from "react";
import { Person, NamesResponse } from "../types";
import "./PeopleSelector.css";

interface PeopleSelectorProps {
    onSelect: (
        type: "plaintiff" | "defendant" | "attorney",
        person: Person
    ) => void;
    selected: {
        plaintiff?: Person;
        defendant?: Person;
        attorney?: Person;
    };
    excelFiles?: File[];
}

export const PeopleSelector: React.FC<PeopleSelectorProps> = ({
    onSelect,
    selected,
    excelFiles,
}) => {
    const [activeTab, setActiveTab] = useState<
        "plaintiff" | "defendant" | "attorney"
    >("plaintiff");
    const [searchTerm, setSearchTerm] = useState("");
    const [names, setNames] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isFocused, setIsFocused] = useState(false);

    useEffect(() => {
        const fetchNames = async () => {
            if (!excelFiles?.length) return;

            setLoading(true);
            setError(null);

            try {
                const formData = new FormData();
                excelFiles.forEach((file) => {
                    formData.append("excel_files", file);
                });

                const response = await fetch(
                    "http://localhost:3000/api/names",
                    {
                        method: "POST",
                        body: formData,
                    }
                );

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data: NamesResponse = await response.json();
                setNames(data.names);
            } catch (err) {
                setError(
                    err instanceof Error ? err.message : "Failed to fetch names"
                );
                console.error("Error fetching names:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchNames();
    }, [excelFiles]);

    const filteredNames = useMemo(() => {
        console.log("Filtering names:", {
            searchTerm,
            names,
            filtered: names.filter((name) =>
                name.toLowerCase().includes(searchTerm.toLowerCase())
            ),
        });

        return names.filter((name) =>
            name.toLowerCase().includes(searchTerm.toLowerCase())
        );
    }, [names, searchTerm]);

    const handleSelect = (name: string) => {
        const person: Person = {
            id: name, // Using name as ID for now
            name: name,
            type: activeTab,
        };
        onSelect(activeTab, person);
        setSearchTerm("");
    };

    useEffect(() => {
        console.log("Search term changed:", searchTerm);
        console.log("Available names:", names);
        console.log("Filtered names:", filteredNames);
    }, [searchTerm, names, filteredNames]);

    const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        console.log("Search input changed:", value);
        setSearchTerm(value.trim()); // Trim whitespace
    };

    return (
        <div className='people-selector'>
            <div className='tabs'>
                <button
                    className={`tab ${
                        activeTab === "plaintiff" ? "active" : ""
                    }`}
                    onClick={() => setActiveTab("plaintiff")}
                >
                    {selected.plaintiff && <span className='selection-dot' />}
                    {selected.plaintiff ? selected.plaintiff.name : "Plaintiff"}
                </button>
                <button
                    className={`tab ${
                        activeTab === "defendant" ? "active" : ""
                    }`}
                    onClick={() => setActiveTab("defendant")}
                >
                    {selected.defendant && <span className='selection-dot' />}
                    {selected.defendant ? selected.defendant.name : "Defendant"}
                </button>
                <button
                    className={`tab ${
                        activeTab === "attorney" ? "active" : ""
                    }`}
                    onClick={() => setActiveTab("attorney")}
                >
                    {selected.attorney && <span className='selection-dot' />}
                    {selected.attorney ? selected.attorney.name : "Attorney"}
                </button>
            </div>
            <div className='search-container'>
                <input
                    type='text'
                    value={searchTerm}
                    onChange={handleSearchChange}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setTimeout(() => setIsFocused(false), 200)}
                    placeholder={`${
                        selected[activeTab] ? "Change" : "Search for"
                    } ${activeTab}...`}
                    className='search-input'
                    disabled={loading || !!error}
                />
                {loading && <div className='loading'>Loading names...</div>}
                {error && <div className='error'>{error}</div>}
                {isFocused && !loading && !error && (
                    <div className='search-results'>
                        {filteredNames.length > 0 ? (
                            filteredNames.map((name) => (
                                <button
                                    key={name}
                                    className='search-result-item'
                                    onClick={() => handleSelect(name)}
                                >
                                    {name}
                                </button>
                            ))
                        ) : (
                            <div className='no-results'>
                                {searchTerm
                                    ? "No matches found"
                                    : "Start typing to filter..."}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};
