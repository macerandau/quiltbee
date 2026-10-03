import Foundation
import Capacitor
import Security
import UIKit

// Two small jobs the web view can't do on its own:
// 1. Keep a few values in the keychain, which survives deleting and reinstalling the app
//    (the free-quilt count lives here so a reinstall doesn't reset it).
// 2. Turn the print sheet (the page's @media print layout) into a PDF and open the share
//    sheet, which has Print, Save to Files, Mail and Messages. window.print() does nothing in WKWebView.
@objc(QuiltBeeNativePlugin)
public class QuiltBeeNativePlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "QuiltBeeNativePlugin"
    public let jsName = "QuiltBeeNative"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "getValue", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "setValue", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "sharePdf", returnType: CAPPluginReturnPromise)
    ]

    private let service = "com.quiltbee.app.state"

    private func baseQuery(_ key: String) -> [String: Any] {
        return [kSecClass as String: kSecClassGenericPassword,
                kSecAttrService as String: service,
                kSecAttrAccount as String: key]
    }

    @objc func getValue(_ call: CAPPluginCall) {
        guard let key = call.getString("key") else { call.reject("key is required"); return }
        var q = baseQuery(key)
        q[kSecReturnData as String] = true
        q[kSecMatchLimit as String] = kSecMatchLimitOne
        var out: AnyObject?
        if SecItemCopyMatching(q as CFDictionary, &out) == errSecSuccess, let d = out as? Data, let s = String(data: d, encoding: .utf8) {
            call.resolve(["value": s])
        } else {
            call.resolve(["value": NSNull()])
        }
    }

    @objc func setValue(_ call: CAPPluginCall) {
        guard let key = call.getString("key"), let value = call.getString("value") else { call.reject("key and value are required"); return }
        let data = Data(value.utf8)
        let q = baseQuery(key)
        let status = SecItemUpdate(q as CFDictionary, [kSecValueData as String: data] as CFDictionary)
        if status == errSecItemNotFound {
            var add = q
            add[kSecValueData as String] = data
            add[kSecAttrAccessible as String] = kSecAttrAccessibleAfterFirstUnlock
            let s2 = SecItemAdd(add as CFDictionary, nil)
            if s2 != errSecSuccess { call.reject("keychain add failed \(s2)"); return }
        } else if status != errSecSuccess {
            call.reject("keychain update failed \(status)"); return
        }
        call.resolve()
    }

    @objc func sharePdf(_ call: CAPPluginCall) {
        let raw = call.getString("name") ?? "Quilt Bee"
        let name = raw.components(separatedBy: CharacterSet(charactersIn: "/\\:?%*|\"<>")).joined(separator: " ").trimmingCharacters(in: .whitespaces)
        DispatchQueue.main.async {
            guard let webView = self.bridge?.webView, let vc = self.bridge?.viewController else { call.reject("no web view"); return }
            // US Letter with half-inch margins; the page's print CSS lays the sheet out.
            let paper = CGRect(x: 0, y: 0, width: 612, height: 792)
            let renderer = UIPrintPageRenderer()
            renderer.addPrintFormatter(webView.viewPrintFormatter(), startingAtPageAt: 0)
            renderer.setValue(paper, forKey: "paperRect")
            renderer.setValue(paper.insetBy(dx: 36, dy: 36), forKey: "printableRect")
            let pdf = NSMutableData()
            UIGraphicsBeginPDFContextToData(pdf, paper, [kCGPDFContextTitle as String: name, kCGPDFContextCreator as String: "Quilt Bee"])
            let pages = renderer.numberOfPages
            renderer.prepare(forDrawingPages: NSRange(location: 0, length: pages))
            for i in 0..<pages {
                UIGraphicsBeginPDFPage()
                renderer.drawPage(at: i, in: UIGraphicsGetPDFContextBounds())
            }
            UIGraphicsEndPDFContext()
            if pages == 0 { call.reject("the print sheet came out empty"); return }

            let url = FileManager.default.temporaryDirectory.appendingPathComponent("\(name.isEmpty ? "Quilt Bee" : name).pdf")
            do { try pdf.write(to: url, options: .atomic) } catch { call.reject("could not write the PDF"); return }

            let share = UIActivityViewController(activityItems: [url], applicationActivities: nil)
            if let pop = share.popoverPresentationController {   // iPad and Mac need an anchor
                pop.sourceView = vc.view
                pop.sourceRect = CGRect(x: vc.view.bounds.midX, y: vc.view.bounds.midY, width: 0, height: 0)
                pop.permittedArrowDirections = []
            }
            share.completionWithItemsHandler = { _, completed, _, _ in
                call.resolve(["completed": completed, "pages": pages])
            }
            vc.present(share, animated: true)
        }
    }
}
