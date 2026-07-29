import { useState } from "react";

function TenderForm({ initialData, onSubmit, buttonText }) {
  const [formData, setFormData] = useState({
    tender_number: initialData?.tender_number || "",
    title: initialData?.title || "",
    department: initialData?.department || "",
    issue_date: initialData?.issue_date || "",
    closing_date: initialData?.closing_date || "",
  });

  function handleChange(e) {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit(formData);
  }

  return (
    <form onSubmit={handleSubmit}>

      <div className="mb-3">
        <label className="form-label">Tender Number</label>
        <input
          type="text"
          name="tender_number"
          className="form-control"
          value={formData.tender_number}
          onChange={handleChange}
          required
        />
      </div>

      <div className="mb-3">
        <label className="form-label">Tender Title</label>
        <input
          type="text"
          name="title"
          className="form-control"
          value={formData.title}
          onChange={handleChange}
          required
        />
      </div>

      <div className="mb-3">
        <label className="form-label">Department</label>
        <input
          type="text"
          name="department"
          className="form-control"
          value={formData.department}
          onChange={handleChange}
          required
        />
      </div>

      <div className="mb-3">
        <label className="form-label">Issue Date</label>
        <input
          type="date"
          name="issue_date"
          className="form-control"
          value={formData.issue_date}
          onChange={handleChange}
          required
        />
      </div>

      <div className="mb-3">
        <label className="form-label">Closing Date</label>
        <input
          type="date"
          name="closing_date"
          className="form-control"
          value={formData.closing_date}
          onChange={handleChange}
          required
        />
      </div>

      <button className="btn btn-primary">
        {buttonText}
      </button>

    </form>
  );
}

export default TenderForm;