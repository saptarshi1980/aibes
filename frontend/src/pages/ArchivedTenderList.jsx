import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getArchivedTenders,
  restoreTender,
} from "../services/tenderService";

function ArchivedTenderList() {

  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    loadTenders();
  }, []);

  async function loadTenders() {

    try {

      const data = await getArchivedTenders();

      setTenders(data);

    } catch (err) {

      console.error(err);

      setError("Unable to load archived tenders.");

    } finally {

      setLoading(false);

    }

  }

  async function handleRestore(tenderId) {

    const confirmed = window.confirm(

      "Restore this Tender?\n\n" +

      "The Tender will be moved back to the Active Tender List.\n\n" +

      "Continue?"

    );

    if (!confirmed) return;

    try {

      await restoreTender(tenderId);

      alert("Tender restored successfully.");

      await loadTenders();

    } catch (err) {

      console.error(err);

      alert("Unable to restore Tender.");

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
        <div className="alert alert-danger">
          {error}
        </div>
      </div>
    );

  }

  return (

    <div className="container mt-4">

      <div className="d-flex justify-content-between align-items-center">

        <h3>Archived Tenders</h3>

        <div>

          <button
            className="btn btn-primary me-2"
            onClick={() => navigate("/tenders")}
          >
            ← Active Tenders
          </button>

          <button
            className="btn btn-secondary"
            onClick={() => navigate("/")}
          >
            🏠 Home
          </button>

        </div>

      </div>

      <div className="alert alert-info mt-3">

        Archived tenders are preserved with all documents,
        bidders, criteria, evaluation reports and clarification
        letters. They may be restored at any time.

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

            <th width="220">Action</th>

          </tr>

        </thead>

        <tbody>

          {tenders.length === 0 ? (

            <tr>

              <td
                colSpan="7"
                className="text-center"
              >
                No Archived Tenders
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

                <td>

                  <span className="badge bg-secondary">
                    {tender.status}
                  </span>

                </td>

                <td>

                  <button
                    className="btn btn-success btn-sm me-2"
                    onClick={() => navigate("/tenders/" + tender.id)}
                  >
                    View
                  </button>

                  <button
                    className="btn btn-warning btn-sm"
                    onClick={() => handleRestore(tender.id)}
                  >
                    Restore
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

export default ArchivedTenderList;