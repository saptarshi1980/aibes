import api from "../api/api";

export async function getAllTenders() {

    const response = await api.get("/tenders");

    return response.data;

}

export async function getTender(id) {

    const response = await api.get("/tenders/" + id);

    return response.data;

}

export async function getTenderDocuments(tenderId) {

    const response = await api.get(
        "/tenders/" + tenderId + "/documents"
    );

    return response.data;

}

export async function getCriteria(tenderId) {

    const response = await api.get(
        "/criteria/" + tenderId
    );

    return response.data;

}

export async function getBidders(tenderId) {

    const response = await api.get(
        "/bidders/tender/" + tenderId
    );

    return response.data;

}

export async function getBidder(bidderId) {

    const response = await api.get(
        "/bidders/" + bidderId
    );

    return response.data;

}

export async function getEvaluationResults(
    bidderId
) {

    const response = await api.get(
        "/evaluation/bidder/" + bidderId
    );

    return response.data;

}

export async function createTender(data) {
    const response = await api.post("/tenders", data);
    return response.data;
}

export async function updateTender(id, data) {
    const response = await api.put(`/tenders/${id}`, data);
    return response.data;
}

export async function uploadTenderDocument(
    tenderId,
    formData
) {

    const response = await api.post(

        `/tenders/${tenderId}/documents`,

        formData,

        {

            headers: {

                "Content-Type": "multipart/form-data"

            }

        }

    );

    return response.data;

}

export async function getBidderDocuments(bidderId) {

    const response = await api.get(

        "/bidders/" + bidderId + "/documents"

    );

    return response.data;

}

export async function uploadBidderDocument(
    bidderId,
    formData
) {

    const response = await api.post(

        "/bidders/" + bidderId + "/documents",

        formData,

        {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }

    );

    return response.data;

}

export async function evaluateBidder(bidderId) {

    const response = await api.post(

        "/evaluation/bidder/" + bidderId

    );

    return response.data;

}

export async function extractCriteria(tenderId) {

    const response = await api.post(
        "/criteria/extract/" + tenderId
    );

    return response.data;

}

export async function deleteTenderDocument(
    documentId
) {

    const response = await api.delete(

        "/tenders/documents/" + documentId

    );

    return response.data;

}

export async function createBidder(data) {

    const response = await api.post(

        "/bidders",

        data

    );

    return response.data;

}

export async function generateBidderIndex(
    bidderId
) {

    const response = await api.post(

        "/bidders/" + bidderId + "/generate-index"

    );

    return response.data;

}

export async function getEmbeddingStatus(
    bidderId
) {

    const response = await api.get(

        "/bidders/" +
        bidderId +
        "/embedding-status"

    );

    return response.data;

}

export async function getEvaluationStatus(bidderId) {

  const response = await api.get(
    `/evaluation/bidder/${bidderId}/status`
  );

  return response.data;
}

export async function deleteBidder(bidderId) {

    const response = await api.delete(

        "/bidders/" + bidderId

    );

    return response.data;

}

export async function getTenderEvaluationReport(
  tenderId
) {

  const response = await api.get(

    "/evaluation/tender/" +
    tenderId +
    "/report"

  );

  return response.data;

}

export async function downloadTenderExcelReport(
    tenderId
) {

    const response = await api.get(

        "/reports/tender/" +
        tenderId +
        "/excel",

        {

            responseType: "blob"

        }

    );

    return response.data;

}



export async function downloadTenderPDFReport(tenderId) {
    const response = await api.get(
        `/tenders/${tenderId}/report`,
        {
            responseType: "blob"
        }
    );
    return response.data;
}

export async function viewTenderDocument(documentId) {

    const response = await api.get(

        `/documents/${documentId}/view`,

        {
            responseType: "blob"
        }

    );

    return response.data;

}

export async function generateClarificationLetter(
    bidderId,
    submissionDate
) {

    const response = await api.post(

        `/evaluation/bidder/${bidderId}/clarification`,

        {
            submission_date: submissionDate
        }

    );

    return response.data;

}