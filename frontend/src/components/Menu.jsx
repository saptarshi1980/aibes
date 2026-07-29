function Menu({ setPage }) {

    return (

        <div
            style={{
                background: "#eeeeee",
                padding: "10px"
            }}
        >

            <button onClick={() => setPage("dashboard")}>
                Dashboard
            </button>

            <button
                onClick={() => setPage("tenders")}
                style={{ marginLeft: "10px" }}
            >
                Tenders
            </button>

            <button
                onClick={() => setPage("bidders")}
                style={{ marginLeft: "10px" }}
            >
                Bidders
            </button>

            <button
                onClick={() => setPage("evaluation")}
                style={{ marginLeft: "10px" }}
            >
                Evaluation
            </button>

        </div>

    );

}

export default Menu;