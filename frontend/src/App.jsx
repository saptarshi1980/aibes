import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";

import Dashboard from "./pages/Dashboard";
import TenderList from "./pages/TenderList";
import BidderList from "./pages/BidderList";
import Evaluation from "./pages/Evaluation";
import TenderDetails from "./pages/TenderDetails";
import EvaluationDetails from "./pages/EvaluationDetails";
import CreateTender from "./pages/CreateTender";
import EditTender from "./pages/EditTender";
import UploadTenderDocument from "./pages/UploadTenderDocument";
import BidderWorkspace from "./pages/BidderWorkspace";
import UploadBidderDocument from "./pages/UploadBidderDocument";
import RegisterBidder from "./pages/RegisterBidder";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />

          <Route path="/tenders" element={<TenderList />} />

          <Route path="/bidders" element={<BidderList />} />

          <Route path="/evaluation" element={<Evaluation />} />
        </Route>

        <Route path="/tenders/:tenderId" element={<TenderDetails />} />

        <Route path="/evaluation/:bidderId" element={<EvaluationDetails />} />

        <Route path="/tenders/new" element={<CreateTender />} />

        <Route path="/tenders/edit/:tenderId" element={<EditTender />} />

        <Route
          path="/tenders/:tenderId/upload-document"
          element={<UploadTenderDocument />}
        />

        <Route path="/bidders/:bidderId" element={<BidderWorkspace />} />

        <Route
          path="/bidders/:bidderId/upload"
          element={<UploadBidderDocument />}
        />

        <Route
          path="/tenders/:tenderId/register-bidder"
          element={<RegisterBidder />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
