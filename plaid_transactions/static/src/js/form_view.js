odoo.define('plaid_transactions.FormView', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var Context = require('web.Context');
    var core = require('web.core');
    var FormController = require('web.FormController');

    var _lt = core._lt;

    var FormView = FormController.include({

        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function (event) {
            if (event.stopPropagation) {
                event.stopPropagation();
            }
            var self = this;
            var attrs = event.data.attrs;
            if (attrs.name === 'plaid_configure') {
                this.saveRecord()
                self._rpc({
                    model: 'account.journal',
                    method: 'fetch_plaid_credentials',
                    context: event.data.record.context,
                    args: [event.data.record.data.id]
                }).then(function (plaid_credentials) {
                    if (!plaid_credentials) {
                        return false;
                    }
                    ajax.loadJS('https://cdn.plaid.com/link/v2/stable/link-initialize.js')
                        .then(function () {
                            var handler = Plaid.create
                            ({
                                token: plaid_credentials.link_token,
                                onSuccess: function (public_token, metadata) {
                                    self._rpc({
                                        model: 'account.journal',
                                        method: 'process_to_be_sync_account',
                                        context: event.data.record.context,
                                        args: [event.data.record.data.id, public_token, metadata.accounts, metadata.institution]
                                    })
                                        .then(function (data) {
                                            window.top.close()
                                            self.do_action(data);
                                        });
                                },
                                onExit: function (err, metadata) {
                                    if (err) {
                                        console.log(err);
                                        console.log(metadata);
                                    }
                                    window.top.close()
                                },
                            });
                            handler.open();
                            return false;
                        });
                });
            } else {
                return this._super.apply(this, arguments);
            }
        },
    });

    return FormView;
});
