import { useEffect, useState } from "react";

import { getAllTenders } from "../services/tenderService";
import { useNavigate } from "react-router-dom";

function TenderList() {
  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    loadTenders();
  }, []);

  async function loadTenders() {
    try {
      const data = await getAllTenders();

      setTenders(data);
    } catch (err) {
      console.error(err);

      setError("Unable to load tenders.");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="container mt-4">
        <h4>Loading...</h4>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger">{error}</div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center">
        <h3>Tender Management</h3>

        <button
          className="btn btn-success"
          onClick={() => navigate("/tenders/new")}
        >
          + Create Tender
        </button>
        <button
        className="btn btn-secondary"
        onClick={() => navigate("/")}
    >
        🏠 Home
    </button>
      </div>

      <table className="table table-bordered table-hover mt-3">
        <thead className="table-dark">
          <tr>
            <th>Tender Number</th>

            <th>Title</th>

            <th>Department</th>

            <th>Issue Date</th>

            <th>Closing Date</th>

            <th>Status</th>

            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {tenders.length === 0 ? (
            <tr>
              <td colSpan="7" className="text-center">
                No Tenders Found
              </td>
            </tr>
          ) : (
            tenders.map((tender) => (
              <tr key={tender.id}>
                <td>{tender.tender_number}</td>

                <td>{tender.title}</td>

                <td>{tender.department}</td>

                <td>{tender.issue_date}</td>

                <td>{tender.closing_date}</td>

                <td>{tender.status}</td>

                <td>
                  <button
                    className="btn btn-success btn-sm me-2"
                    onClick={() => navigate("/tenders/" + tender.id)}
                  >
                    View
                  </button>

                  <button
                    className="btn btn-warning btn-sm"
                    onClick={() => navigate("/tenders/edit/" + tender.id)}
                  >
                    Edit
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default TenderList;
