#stat-panel {
    margin-top: 12px;
    font-size: 12px;
    height: auto;
    max-height: 110px;
    overflow: auto;
    background-color: #f5f7fa;
    border-radius: 6px;
    padding: 10px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    border: 1px solid #d1d8e0;
}

#stat-panel h3 {
    font-size: 14px;
    margin-bottom: 8px;
    color: #2c3e50;
    border-bottom: 1px solid #d1d8e0;
    padding-bottom: 5px;
}

#stat-panel p {
    font-size: 11px;
    margin: 5px 0;
    padding: 5px 8px;
    border-radius: 4px;
    transition: all 0.2s ease;
    cursor: pointer;
    background-color: white;
    border: 1px solid #e0e5ec;
}

#stat-panel p:hover {
    background-color: #e3e8ed;
    border-color: #3498db;
}

#stat-panel p.active-filter {
    background-color: #e3f9e5;
    border-color: #27ae60;
    font-weight: 500;
}

#skottlossningar {
    color: #e74c3c;
    border-left: 2px solid #e74c3c;
}

#sprangningar {
    color: #f39c12;
    border-left: 2px solid #f39c12;
}

#mord {
    color: #c0392b;
    border-left: 2px solid #c0392b;
}

@media (max-width: 768px) {
    #stat-panel {
        padding: 8px;
        font-size: 11px;
    }

    #stat-panel h3 {
        font-size: 13px;
    }

    #stat-panel p {
        font-size: 10px;
        padding: 4px 6px;
    }
}