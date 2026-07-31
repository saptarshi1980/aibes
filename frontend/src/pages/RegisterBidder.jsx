import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";

import BidderForm from "../components/BidderForm";

import { createBidder } from "../services/tenderService";

function RegisterBidder() {

    const { tenderId } = useParams();

    const navigate = useNavigate();

    async function saveBidder(data) {

        try {

            const bidder = await createBidder({

                tender_id: tenderId,

                bidder_name: data.bidder_name,

                contact_person: data.contact_person,

                email: data.email,

                phone: data.phone

            });

            alert(
                "Bidder registered successfully."
            );

            navigate(
                "/bidders/" + bidder.id
            );

        }

        catch (err) {

            console.error(err);

            alert(

                err.response?.data?.detail ||

                "Unable to register bidder."

            );

        }

    }

    return (

        <div className="container mt-4">

            <div className="card">

                <div className="card-header bg-primary text-white">

                    Register Bidder

                </div>

                <div className="card-body">

                    <BidderForm

                        onSubmit={saveBidder}

                        buttonText="Register Bidder"

                    />

                </div>

            </div>

        </div>

    );

}

export default RegisterBidder;